import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

from dreamapi import DreamAPI, ProviderError, SubmissionUncertain
import jobs
from mask_review import FILES, fingerprint, review


class DreamAPITests(unittest.TestCase):
    def test_submission_uses_platform_contract_and_no_draft_fields(self):
        response = Mock(status_code=200)
        response.json.return_value = {"code": 0, "data": {"taskId": "task-1"}}
        with patch("dreamapi.requests.post", return_value=response) as post:
            ident = DreamAPI("private-key").submit({"model": "seedance-2.5", "resolution": "1080p"})
        self.assertEqual(ident, "task-1")
        self.assertTrue(post.call_args.args[0].endswith("/api/async/seedance_2.5"))
        self.assertNotIn("is_draft", post.call_args.kwargs["json"])
        self.assertNotIn("draft_id", post.call_args.kwargs["json"])

    def test_submission_timeouts_and_missing_task_ids_are_uncertain(self):
        with patch("dreamapi.requests.post", side_effect=requests.Timeout):
            with self.assertRaises(SubmissionUncertain):
                DreamAPI("key").submit({})
        response = Mock(status_code=200)
        response.json.return_value = {"code": 0, "data": {}}
        with patch("dreamapi.requests.post", return_value=response):
            with self.assertRaises(SubmissionUncertain):
                DreamAPI("key").submit({})

    def test_explicit_provider_rejection_is_not_a_submission_success(self):
        response = Mock(status_code=200)
        response.json.return_value = {"code": 402, "message": "credits required"}
        with patch("dreamapi.requests.post", return_value=response):
            with self.assertRaises(ProviderError) as error:
                DreamAPI("key").submit({})
        self.assertEqual(error.exception.code, 402)


class DurableJobsTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.root = Path(self.directory.name)
        self.patch = patch.object(jobs, "RUNS", self.root)
        self.patch.start()
        jobs.STOP.clear()
        self.ident = "b" * 32
        self.folder = self.root / self.ident
        self.folder.mkdir()
        for name in FILES:
            (self.folder / name).write_bytes(b"video")
        (self.folder / "reference-1.png").write_bytes(b"image")
        jobs.write_json(self.folder / "job.json", {
            "id": self.ident, "created_at": "2026-11-11T00:00:00+00:00", "name": "source.mp4",
            "state": "submitting", "stage": "upload", "mode": "depth", "duration": 5.3,
            "resolution": "1080p", "ratio": "16:9", "reference_files": ["reference-1.png"],
            "prompt": "Replace the character",
        })
        review(self.folder, True, "Reviewed", fingerprint(self.folder))

    def tearDown(self):
        self.patch.stop()
        self.directory.cleanup()

    def test_task_saved_before_collection_and_not_resubmitted(self):
        client = Mock()
        client.upload.return_value = "https://media.example/input"
        client.submit.return_value = "saved-task"
        with patch("jobs.DreamAPI", return_value=client), patch("jobs.credential", return_value="key"), patch("jobs.collect") as collect:
            jobs.generate(self.ident)
            self.assertEqual(jobs.read_job(self.ident)["task_id"], "saved-task")
            self.assertEqual(json.loads((self.folder / "generation.json").read_text())["task_id"], "saved-task")
            collect.assert_called_once_with(self.ident)
            payload = client.submit.call_args.args[0]
            self.assertEqual(payload["resolution"], "1080p")
            self.assertEqual(payload["videos"], ["https://media.example/input"])
            self.assertNotIn("is_draft", payload)
            with self.assertRaises(SubmissionUncertain):
                jobs.generate(self.ident)
        self.assertEqual(client.submit.call_count, 1)

    def test_uncertain_submission_survives_restart_without_requeue(self):
        client = Mock()
        client.upload.return_value = "https://media.example/input"
        client.submit.side_effect = SubmissionUncertain()
        with patch("jobs.DreamAPI", return_value=client), patch("jobs.credential", return_value="key"):
            with self.assertRaises(SubmissionUncertain):
                jobs.generate(self.ident)
        self.assertTrue((self.folder / "submission.json").exists())
        with patch("jobs.start_worker") as worker:
            jobs.recover()
        self.assertEqual(jobs.read_job(self.ident)["state"], "uncertain")
        worker.assert_not_called()

    def test_recovery_collects_saved_task_without_submission(self):
        jobs.update(self.ident, state="generating", task_id="existing")
        with patch("jobs.start_worker") as worker:
            jobs.recover()
        worker.assert_called_once()

    def test_status_does_not_expose_provider_task_id(self):
        jobs.update(self.ident, task_id="private-provider-id", state="ready")
        self.assertNotIn("task_id", jobs.public_job(self.ident))


if __name__ == "__main__":
    unittest.main()
