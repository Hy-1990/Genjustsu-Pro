"""Durable Replicate prediction collection. Only read requests are retried."""
import json
from pathlib import Path
import time
import uuid

import requests


class PreparationUncertain(RuntimeError):
    pass


def save_prediction(path, data):
    path = Path(path)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(data, indent=2))
    temporary.replace(path)


def read_prediction(path):
    return json.loads(Path(path).read_text())


def submission_marker(path):
    path = Path(path)
    return path.with_name(path.stem + "-submission.json")


def get_response(url, headers):
    for attempt in range(6):
        try:
            response = requests.get(url, headers=headers, timeout=(10, 30))
            response.raise_for_status()
            return response
        except requests.RequestException as exc:
            code = exc.response.status_code if exc.response is not None else None
            if code is not None and code not in (429, 500, 502, 503, 504):
                raise
            if attempt == 5:
                raise
            time.sleep(min(2 ** attempt, 10))
    raise RuntimeError("Unreachable")


def submit_prediction(path, headers, payload):
    path = Path(path)
    if path.exists():
        return read_prediction(path)
    marker = submission_marker(path)
    if marker.exists():
        raise PreparationUncertain("preparation_uncertain")
    save_prediction(marker, {"attempted_at": time.time()})
    try:
        response = requests.post("https://api.replicate.com/v1/predictions", headers=headers, json=payload, timeout=(10, 60))
    except requests.RequestException as exc:
        raise PreparationUncertain("preparation_uncertain") from exc
    if response.status_code >= 500:
        raise PreparationUncertain("preparation_uncertain")
    if response.status_code >= 400:
        marker.unlink(missing_ok=True)
        response.raise_for_status()
    try:
        prediction = response.json()
    except ValueError as exc:
        raise PreparationUncertain("preparation_uncertain") from exc
    if not isinstance(prediction, dict) or not prediction.get("id") or not prediction.get("urls", {}).get("get"):
        raise PreparationUncertain("preparation_uncertain")
    save_prediction(path, prediction)
    marker.unlink(missing_ok=True)
    return prediction


def wait_prediction(path, headers, status=print):
    prediction = read_prediction(path)
    deadline = time.monotonic() + 1800
    while time.monotonic() < deadline:
        prediction = get_response(prediction["urls"]["get"], headers).json()
        save_prediction(path, prediction)
        state = prediction.get("status", "starting")
        status("cloud:" + state)
        if state == "succeeded":
            return prediction
        if state in ("failed", "canceled"):
            raise RuntimeError("Replicate prediction " + state)
        time.sleep(5)
    raise TimeoutError("preparation_timeout")
