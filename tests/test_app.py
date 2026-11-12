import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from fastapi.testclient import TestClient
from PIL import Image

import app
import jobs
from mask_review import FILES, fingerprint, review


class LocalAppTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.run_patch = patch.object(jobs, "RUNS", Path(self.directory.name))
        self.run_patch.start()
        self.secrets = {}
        self.key_patch = patch("credential_store.get_key", side_effect=lambda provider: self.secrets.get(provider, ""))
        self.key_patch.start()
        self.save_patch = patch("credential_store.save_key", side_effect=lambda provider, value: self.secrets.update({provider: value}))
        self.save_patch.start()
        self.delete_patch = patch("credential_store.delete_key", side_effect=lambda provider: self.secrets.pop(provider, None))
        self.delete_patch.start()
        self.client = TestClient(app.app)
        self.client.__enter__()
        self.headers = {"X-Local-Token": self.client.get("/api/session").json()["token"]}

    def tearDown(self):
        self.client.__exit__(None, None, None)
        self.delete_patch.stop()
        self.save_patch.stop()
        self.key_patch.stop()
        self.run_patch.stop()
        self.directory.cleanup()

    def make_job(self, approved=True):
        ident = "a" * 32
        folder = jobs.RUNS / ident
        folder.mkdir()
        for name in FILES:
            (folder / name).write_bytes(b"media")
        (folder / "upload.mp4").write_bytes(b"source")
        jobs.write_json(folder / "job.json", {
            "id": ident, "name": "test.mp4", "created_at": "2026-11-11T00:00:00+00:00",
            "state": "ready" if approved else "review", "stage": "review", "mode": "depth",
            "subject": "person", "duration": 5.3, "width": 960, "height": 540, "error": None,
        })
        if approved:
            review(folder, True, "Entire clip inspected", fingerprint(folder))
        return ident, folder

    def test_key_api_never_echoes_secret_and_checks_session_origin(self):
        self.assertEqual(self.client.put("/api/keys/dreamapi", json={"value": "secret"}).status_code, 403)
        response = self.client.put("/api/keys/dreamapi", json={"value": "secret"}, headers=self.headers)
        self.assertEqual(response.json(), {"configured": True})
        status = self.client.get("/api/keys")
        self.assertEqual(status.json()["providers"]["dreamapi"], True)
        self.assertNotIn("secret", status.text)
        bad = {**self.headers, "Origin": "https://attacker.example"}
        self.assertEqual(self.client.delete("/api/keys/dreamapi", headers=bad).status_code, 403)
        self.assertEqual(self.client.delete("/api/keys/dreamapi", headers=self.headers).status_code, 200)

    def test_generate_requires_exact_review_and_direct_resolution(self):
        self.secrets["dreamapi"] = "test-key"
        ident, folder = self.make_job()
        image = io.BytesIO()
        Image.new("RGB", (32, 32)).save(image, format="PNG")
        with patch("jobs.start_worker") as worker:
            response = self.client.post(
                f"/api/jobs/{ident}/generate", headers=self.headers,
                data={"prompt": "Replace the person", "resolution": "1080p"},
                files={"reference": ("identity.png", image.getvalue(), "image/png")},
            )
        self.assertEqual(response.status_code, 200, response.text)
        self.assertEqual(jobs.read_job(ident)["resolution"], "1080p")
        worker.assert_called_once()
        # A second request is blocked even before a provider response exists.
        again = self.client.post(f"/api/jobs/{ident}/generate", headers=self.headers,
            data={"prompt": "Replace", "resolution": "1080p"},
            files={"reference": ("identity.png", image.getvalue(), "image/png")})
        self.assertEqual(again.status_code, 409)

    def test_changed_input_blocks_generation_and_private_files(self):
        self.secrets["dreamapi"] = "test-key"
        ident, folder = self.make_job()
        (folder / "seedance-input.mp4").write_bytes(b"changed")
        with patch("jobs.start_worker") as worker:
            response = self.client.post(f"/api/jobs/{ident}/generate", headers=self.headers,
                data={"prompt": "Replace", "resolution": "720p"},
                files={"reference": ("identity.png", b"image", "image/png")})
        self.assertEqual(response.status_code, 409)
        worker.assert_not_called()
        self.assertEqual(self.client.get(f"/api/jobs/{ident}/files/job.json").status_code, 404)
        self.assertEqual(self.client.get(f"/api/jobs/{ident}/files/upload.mp4").status_code, 200)

    def test_nonexistent_job_and_missing_key_are_actionable(self):
        self.assertEqual(self.client.get("/api/jobs/" + "f" * 32).status_code, 404)
        response = self.client.post("/api/jobs", headers=self.headers, files={"video": ("source.mp4", b"bad")})
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()["detail"], "keys_required")

    def test_preparation_resume_reuses_saved_tasks_and_blocks_ambiguous_submit(self):
        self.secrets["replicate"] = "test-key"
        ident, folder = self.make_job(False)
        jobs.write_json(folder / "depth-prediction.json", {"id": "existing", "status": "processing"})
        jobs.update(ident, state="error", stage="depth", error="network_error")
        with patch("jobs.start_worker") as worker:
            result = self.client.post(f"/api/jobs/{ident}/resume-preparation", headers=self.headers)
        self.assertEqual(result.status_code, 200)
        worker.assert_called_once()
        self.assertEqual(json.loads((folder / "depth-prediction.json").read_text())["id"], "existing")
        jobs.update(ident, state="error", error="preparation_uncertain")
        jobs.write_json(folder / "sam-raw-request-submission.json", {"attempted_at": 1})
        with patch("jobs.start_worker") as worker:
            result = self.client.post(f"/api/jobs/{ident}/resume-preparation", headers=self.headers)
        self.assertEqual(result.status_code, 409)
        worker.assert_not_called()

    def test_paid_stage_retry_requires_confirmed_failure_and_no_ambiguous_submit(self):
        from unittest.mock import Mock
        self.secrets["replicate"] = "test-key"
        ident, folder = self.make_job(False)
        saved = {"id": "existing", "status": "failed", "urls": {"get": "https://api.replicate.com/v1/predictions/existing"}}
        jobs.write_json(folder / "depth-prediction.json", saved)
        jobs.update(ident, state="error", stage="depth", error="processing_error")
        response = Mock(); response.json.return_value = {**saved, "status": "processing"}
        with patch("replicate_jobs.get_response", return_value=response), patch("jobs.start_worker") as worker:
            result = self.client.post(f"/api/jobs/{ident}/retry-preparation", headers=self.headers)
        self.assertEqual(result.status_code, 409)
        worker.assert_not_called()
        jobs.write_json(folder / "depth-prediction.json", saved)
        jobs.write_json(folder / "sam-raw-request-submission.json", {"attempted_at": 1})
        with patch("replicate_jobs.get_response") as get, patch("jobs.start_worker") as worker:
            result = self.client.post(f"/api/jobs/{ident}/retry-preparation", headers=self.headers)
        self.assertEqual(result.status_code, 409)
        worker.assert_not_called(); get.assert_not_called()

    def test_repair_resume_keeps_the_repair_path(self):
        self.secrets["replicate"] = "test-key"
        ident, folder = self.make_job(False)
        jobs.write_json(folder / "depth-prediction.json", {"id": "saved"})
        jobs.update(ident, state="error", stage="mask", error="network_error", preparation_action="repair")
        with patch("jobs.start_worker") as worker, patch("jobs.repair") as repair:
            result = self.client.post(f"/api/jobs/{ident}/resume-preparation", headers=self.headers)
            worker.call_args.args[1]()
        self.assertEqual(result.json()["state"], "repairing")
        repair.assert_called_once_with(ident)
        self.assertEqual(jobs.preparation_prediction_path(folder, jobs.read_job(ident), "mask"), folder / "rgb-repair/sam-raw-request.json")

    def test_review_waits_for_human_and_repair_does_not_show_old_mask_as_done(self):
        ident, folder = self.make_job(False)
        stages = {item["id"]: item["state"] for item in jobs.public_job(ident)["pipeline"]}
        self.assertEqual(stages["review"], "waiting")
        jobs.update(ident, state="repairing", stage="mask")
        stages = {item["id"]: item["state"] for item in jobs.public_job(ident)["pipeline"]}
        self.assertEqual(stages["mask"], "active")
        self.assertEqual(stages["composite"], "pending")

    def test_preparing_job_exposes_no_partial_review(self):
        ident, folder = self.make_job(False)
        jobs.update(ident, state="preparing")
        response = self.client.get(f"/api/jobs/{ident}").json()
        self.assertNotIn("review", response)


if __name__ == "__main__":
    unittest.main()
