"""DreamAPI Seedance 2.5 and storage, following the platform's skill client contract."""
from pathlib import Path
from urllib.parse import urlparse

import requests

BASE_URL = "https://api.newportai.com"


class ProviderError(RuntimeError):
    def __init__(self, message, code=None):
        super().__init__(message)
        self.code = code


class SubmissionUncertain(RuntimeError):
    pass


class DreamAPI:
    def __init__(self, key):
        self.key = key

    def post(self, endpoint, body, *, submission=False):
        try:
            response = requests.post(
                BASE_URL + endpoint,
                headers={"Authorization": f"Bearer {self.key}", "Content-Type": "application/json"},
                json=body,
                timeout=(15, 120),
            )
        except requests.RequestException as exc:
            if submission:
                raise SubmissionUncertain("submission_uncertain") from exc
            raise
        if submission and response.status_code >= 500:
            raise SubmissionUncertain("submission_uncertain")
        try:
            response.raise_for_status()
        except requests.HTTPError as exc:
            raise ProviderError("DreamAPI request failed", response.status_code) from exc
        try:
            payload = response.json()
        except ValueError as exc:
            if submission:
                raise SubmissionUncertain("submission_uncertain") from exc
            raise ProviderError("Invalid DreamAPI response") from exc
        if payload.get("code") != 0:
            raise ProviderError("DreamAPI rejected request", payload.get("code"))
        data = payload.get("data")
        if not isinstance(data, dict):
            if submission:
                raise SubmissionUncertain("submission_uncertain")
            raise ProviderError("Invalid DreamAPI data")
        return data

    def upload(self, filename):
        filename = Path(filename)
        policy = self.post("/api/file/v1/get_policy", {"scene": "Dream-CN"})
        host = policy.get("host", "")
        key = policy.get("key") or (policy.get("dir", "") + filename.name)
        access_id = policy.get("accessId") or policy.get("OSSAccessKeyId")
        if urlparse(host).scheme != "https" or not all(
            [key, access_id, policy.get("policy"), policy.get("signature")]
        ):
            raise ProviderError("Invalid upload policy")
        fields = {
            "key": key,
            "policy": policy["policy"],
            "OSSAccessKeyId": access_id,
            "signature": policy["signature"],
            "callback": policy.get("callback", ""),
            "success_action_status": "200",
        }
        with filename.open("rb") as media:
            response = requests.post(host, data=fields, files={"file": (filename.name, media)}, timeout=(15, 300))
        response.raise_for_status()
        uploaded = response.json()
        request_id = uploaded.get("data", {}).get("reqId") or policy.get("reqId")
        if not request_id:
            raise ProviderError("Upload request ID missing")
        result = self.post("/api/file/v1/policy_upload_finish", {"reqId": request_id})
        url = result.get("url", "")
        if urlparse(url).scheme != "https":
            raise ProviderError("Uploaded media URL missing")
        return url

    def submit(self, payload):
        data = self.post("/api/async/seedance_2.5", payload, submission=True)
        task_id = data.get("taskId")
        if not isinstance(task_id, str) or not task_id:
            raise SubmissionUncertain("submission_uncertain")
        return task_id

    def query(self, task_id):
        return self.post("/api/getAsyncResult", {"taskId": task_id})

    def download(self, url, target):
        if urlparse(url).scheme != "https":
            raise ProviderError("Invalid result URL")
        target = Path(target)
        temporary = target.with_suffix(".partial")
        try:
            with requests.get(url, stream=True, timeout=(15, 180)) as response:
                response.raise_for_status()
                with temporary.open("wb") as output:
                    for chunk in response.iter_content(1024 * 1024):
                        output.write(chunk)
            if not temporary.stat().st_size:
                raise ProviderError("Empty result")
            temporary.replace(target)
        finally:
            temporary.unlink(missing_ok=True)
