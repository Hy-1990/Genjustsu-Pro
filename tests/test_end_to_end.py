"""Exercise the normal HTTP flow with synthetic media and mocked paid providers."""
import io
import json
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest.mock import Mock, patch

from fastapi.testclient import TestClient
from PIL import Image

import app
import jobs
from mask_review import FILES
from test_audio_alignment import audio_packets, clip


class FullWorkflowTests(unittest.TestCase):
    def test_upload_review_generate_download_keeps_original_audio_without_drafts(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            runs = root / "runs"
            runs.mkdir()
            clip(root / "source.mp4", 103, audio=True)
            clip(root / "generated.mp4", 96)

            def prepare(ident):
                folder = jobs.folder_for(ident)
                for name in FILES:
                    shutil.copy2(folder / "upload.mp4", folder / name)
                jobs.update(ident, state="review", stage="review")

            provider = Mock()
            provider.upload.return_value = "https://media.example/input"
            provider.submit.return_value = "existing-task"
            provider.query.return_value = {"task": {"status": 3}, "videos": [{"videoUrl": "https://media.example/result.mp4"}]}
            provider.download.side_effect = lambda url, target: shutil.copy2(root / "generated.mp4", target)
            image = io.BytesIO()
            Image.new("RGB", (64, 64)).save(image, format="PNG")

            with patch.object(jobs, "RUNS", runs), patch("credential_store.get_key", return_value="test-key"), \
                    patch("jobs.credential", return_value="test-key"), patch("jobs.prepare", side_effect=prepare), \
                    patch("jobs.DreamAPI", return_value=provider), \
                    patch("jobs.start_worker", side_effect=lambda ident, action: action()), TestClient(app.app) as client:
                headers = {"X-Local-Token": client.get("/api/session").json()["token"]}
                created = client.post("/api/jobs", headers=headers,
                    data={"mode": "depth", "subject": "person"},
                    files={"video": ("source.mp4", (root / "source.mp4").read_bytes(), "video/mp4")})
                self.assertEqual(created.status_code, 201, created.text)
                ident = created.json()["id"]
                current = client.get(f"/api/jobs/{ident}").json()
                approved = client.post(f"/api/jobs/{ident}/review", headers=headers,
                    json={"approved": True, "fingerprint": current["review"]["fingerprint"]})
                self.assertEqual(approved.status_code, 200)
                generated = client.post(f"/api/jobs/{ident}/generate", headers=headers,
                    data={"prompt": "Replace the person with the supplied character.", "resolution": "1080p"},
                    files={"reference": ("character.png", image.getvalue(), "image/png")})
                self.assertEqual(generated.status_code, 200, generated.text)
                completed = client.get(f"/api/jobs/{ident}").json()
                self.assertEqual(completed["state"], "done")
                self.assertTrue(completed["duration_adjusted"])
                downloaded = client.get(f"/api/jobs/{ident}/files/final-preview.mp4")
                self.assertEqual(downloaded.status_code, 200)
                self.assertEqual(audio_packets(root / "source.mp4"), audio_packets(runs / ident / "final-preview.mp4"))
                payload = provider.submit.call_args.args[0]
                self.assertEqual(payload["resolution"], "1080p")
                self.assertNotIn("is_draft", payload)
                self.assertNotIn("draft_id", payload)
                self.assertEqual(provider.submit.call_count, 1)
                job_data = json.loads((runs / ident / "job.json").read_text())
                self.assertEqual(job_data["task_id"], "existing-task")
                for path in (runs / ident).glob("*.json"):
                    self.assertNotIn("test-key", path.read_text())


if __name__ == "__main__":
    unittest.main()
