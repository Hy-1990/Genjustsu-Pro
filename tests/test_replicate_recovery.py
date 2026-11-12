import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import Mock, patch

import requests

import replicate_jobs
from pipeline import depth_replicate


class ReplicateRecoveryTests(unittest.TestCase):
    def test_transient_poll_failure_retries_only_the_same_read_request(self):
        response = Mock()
        response.json.return_value = {"id": "saved", "status": "succeeded", "output": "https://result.example/depth.mp4", "urls": {"get": "https://api.replicate.com/v1/predictions/saved"}}
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "depth-prediction.json"
            replicate_jobs.save_prediction(path, {"id": "saved", "urls": {"get": "https://api.replicate.com/v1/predictions/saved"}})
            with patch("replicate_jobs.requests.get", side_effect=[requests.ReadTimeout(), response]) as get, patch("replicate_jobs.requests.post") as post, patch("replicate_jobs.time.sleep"):
                result = replicate_jobs.wait_prediction(path, {}, status=lambda text: None)
            self.assertEqual(result["status"], "succeeded")
            self.assertEqual(get.call_count, 2)
            post.assert_not_called()
            self.assertEqual(json.loads(path.read_text())["status"], "succeeded")

    def test_known_prediction_is_never_submitted_again(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "audio-prediction.json"
            replicate_jobs.save_prediction(path, {"id": "existing"})
            with patch("replicate_jobs.requests.post") as post:
                result = replicate_jobs.submit_prediction(path, {}, {})
            self.assertEqual(result["id"], "existing")
            post.assert_not_called()

    def test_uncertain_submit_blocks_automatic_resubmission(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "depth-prediction.json"
            with patch("replicate_jobs.requests.post", side_effect=requests.ReadTimeout()) as post:
                with self.assertRaises(replicate_jobs.PreparationUncertain):
                    replicate_jobs.submit_prediction(path, {}, {})
                with self.assertRaises(replicate_jobs.PreparationUncertain):
                    replicate_jobs.submit_prediction(path, {}, {})
            self.assertEqual(post.call_count, 1)

    def test_cached_depth_does_not_call_cloud_or_rebill(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "depth-raw.mp4"
            output.write_bytes(b"downloaded-depth")
            with patch("replicate_jobs.requests.post") as post, patch("replicate_jobs.requests.get") as get:
                depth_replicate("source.mp4", output)
            post.assert_not_called()
            get.assert_not_called()

    def test_authentication_errors_are_not_hidden_by_network_retries(self):
        response = requests.Response()
        response.status_code = 401
        with patch("replicate_jobs.requests.get", return_value=response) as get:
            with self.assertRaises(requests.HTTPError):
                replicate_jobs.get_response("https://api.replicate.com/v1/predictions/saved", {})
        get.assert_called_once()


if __name__ == "__main__":
    unittest.main()
