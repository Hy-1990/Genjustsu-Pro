"""A single-process durable job runner. Paid submissions are never retried implicitly."""
from datetime import datetime, timezone
import json
from pathlib import Path
import threading
import time
import uuid

import av
import requests

from config import ROOT, credential
from dreamapi import DreamAPI, ProviderError, SubmissionUncertain
from mask_review import state as review_state, require_approved

RUNS = ROOT / "runs"
RUNS.mkdir(exist_ok=True)
_lock = threading.RLock()
_active = set()
STOP = threading.Event()
MODES = ("depth", "face_mesh", "depth_mesh")


def write_json(path, data):
    path = Path(path)
    temporary = path.with_name(path.name + "." + uuid.uuid4().hex + ".tmp")
    temporary.write_text(json.dumps(data, ensure_ascii=False, indent=2))
    temporary.replace(path)


def folder_for(ident):
    if len(ident) != 32 or any(char not in "0123456789abcdef" for char in ident):
        raise FileNotFoundError("Job not found")
    folder = RUNS / ident
    if not folder.is_dir():
        raise FileNotFoundError("Job not found")
    return folder


def read_job(ident):
    return json.loads((folder_for(ident) / "job.json").read_text())


def update(ident, **changes):
    with _lock:
        data = read_job(ident)
        data.update(changes, updated_at=datetime.now(timezone.utc).isoformat())
        write_json(folder_for(ident) / "job.json", data)
        return data


def inspect_video(path, *, source=False):
    with av.open(str(path)) as video:
        if not video.streams.video:
            raise ValueError("invalid_video")
        stream = video.streams.video[0]
        duration = float(stream.duration * stream.time_base) if stream.duration else float(video.duration / av.time_base)
        if not (4 if source else 2) <= duration <= 30:
            raise ValueError("duration_range")
        if source and not video.streams.audio:
            raise ValueError("audio_required")
        return {"duration": duration, "width": stream.width, "height": stream.height}


def public_job(ident):
    data = read_job(ident)
    folder = folder_for(ident)
    data["can_resume"] = data["state"] == "error" and bool(data.get("task_id") or (folder / "generation.json").exists())
    data["task_submitted"] = (folder / "submission.json").exists() or (folder / "generation.json").exists()
    data.pop("task_id", None)
    data["files"] = [
        name for name in ("upload.mp4", "original.mp4", "depth.mp4", "mask.mp4",
                          "seedance-input.mp4", "final-preview.mp4")
        if (folder / name).is_file()
    ]
    data["references"] = [name for name in data.get("reference_files", []) if (folder / name).is_file()]
    if data["state"] in ("review", "ready", "error"):
        data["review"] = review_state(folder)
    return data


def list_jobs():
    result = []
    for path in RUNS.glob("*/job.json"):
        try:
            data = read_job(path.parent.name)
            result.append({key: data.get(key) for key in ("id", "name", "created_at", "state", "mode", "resolution")})
        except (ValueError, OSError):
            continue
    return sorted(result, key=lambda item: item["created_at"], reverse=True)


def error_code(exc):
    if isinstance(exc, ProviderError):
        if exc.code in (401, 403):
            return "provider_auth"
        if exc.code == 402:
            return "provider_payment"
        return "provider_error"
    if isinstance(exc, requests.HTTPError):
        if exc.response is not None:
            if exc.response.status_code == 402:
                return "provider_payment"
            if exc.response.status_code in (401, 403):
                return "provider_auth"
        return "provider_error"
    if isinstance(exc, requests.RequestException):
        return "network_error"
    if isinstance(exc, TimeoutError):
        return "collection_timeout"
    if isinstance(exc, ValueError) and str(exc).startswith("missing_"):
        return "keys_required"
    return "processing_error"


def start_worker(ident, action):
    with _lock:
        if ident in _active:
            raise ValueError("job_busy")
        _active.add(ident)

    def run():
        try:
            action()
        except SubmissionUncertain:
            update(ident, state="uncertain", stage="uncertain", error="submission_uncertain")
        except Exception as exc:
            folder = folder_for(ident)
            if (folder / "submission.json").exists() and not (folder / "generation.json").exists():
                update(ident, state="uncertain", stage="uncertain", error="submission_uncertain")
                return
            # Provider messages and signed URLs are deliberately kept out of the UI and logs.
            update(ident, state="error", error=error_code(exc))
        finally:
            with _lock:
                _active.discard(ident)
    thread = threading.Thread(target=run, daemon=True, name="job-" + ident)
    thread.start()


def progress(ident, message):
    lower = message.lower()
    stage = "prepare"
    for fragment, candidate in (("audio", "audio"), ("vocal", "audio"), ("pitch", "audio"),
                                ("depth", "depth"), ("sam", "mask"), ("segment", "mask"),
                                ("composit", "composite"), ("mesh", "mesh")):
        if fragment in lower:
            stage = candidate
    update(ident, stage=stage)


def prepare(ident):
    folder = folder_for(ident)
    data = read_job(ident)
    mode = data["mode"]
    callback = lambda message: progress(ident, message)
    if mode == "face_mesh":
        from face_mesh import run
        run(folder / "upload.mp4", folder, callback)
    elif mode == "depth_mesh":
        from face_mesh import run_depth
        run_depth(folder / "upload.mp4", folder, data["subject"], "replicate", callback)
    else:
        from pipeline import run
        run(folder / "upload.mp4", folder, data["subject"], "replicate", callback)
    update(ident, state="review", stage="review", error=None)


def repair(ident):
    folder = folder_for(ident)
    data = read_job(ident)
    if data["mode"] == "face_mesh":
        raise ValueError("mesh_no_mask")
    from raw_masks import segment_raw, clean_border_fragments
    from pipeline import composite
    from audio_workflow import prepare_seedance_video
    (folder / "rgb-repair").mkdir(exist_ok=True)
    masks = clean_border_fragments(segment_raw(folder / "original.mp4", folder / "rgb-repair", data["subject"]))
    composite(folder / "original.mp4", folder / "depth.mp4", masks, folder, folder / "upload.mp4")
    if data["mode"] == "depth_mesh":
        import shutil
        from face_mesh import track
        shutil.copy2(folder / "composite-silent.mp4", folder / "depth-composite-silent.mp4")
        track(folder, combined=True)
    prepare_seedance_video(folder)
    (folder / "mask-review.json").unlink(missing_ok=True)
    update(ident, state="review", stage="review", error=None)



def generation_prompt(prompt, *, identity_video, second_reference, mode):
    """Preserve the upstream model instructions independently of interface localization."""
    if identity_video:
        result = prompt + (
            "\n@Video1 is the source edit and contains isolated vocals pitched +3 semitones. "
            "@Video2 is only the primary character visual identity reference. "
            "Use only @Video1 audio for speech timing."
        )
    else:
        mapping = (
            "@Image1 is the primary character reference; @Image2 is the secondary character reference."
            if second_reference else "@Image1 is the only replacement character reference."
        )
        result = prompt.replace("@Audio1", "the audio embedded in @Video1") + (
            "\n@Video1 contains the colored-depth composite and embedded isolated vocals pitched up three semitones, "
            "without the music bed; use its embedded audio for performance and lip synchronization. "
        ) + mapping
    if mode in ("face_mesh", "depth_mesh"):
        description = "depth composite with face mesh overlay" if mode == "depth_mesh" else "original video with face mesh overlay"
        result = result.replace("colored-depth composite", description) + (
            " Remove all face mesh lines and any depth colors from the output; "
            "use them only for expression and lip motion guidance. "
            "Replace the entire original identity including hair. Preserve the exact embedded dialogue and timing."
        )
    return result


def generate(ident):
    folder = folder_for(ident)
    require_approved(folder)
    client = DreamAPI(credential("DREAMAPI_API_KEY"))
    data = read_job(ident)
    if (folder / "submission.json").exists():
        raise SubmissionUncertain("submission_uncertain")
    update(ident, stage="upload")
    prepared_url = client.upload(folder / "seedance-input.mp4")
    references = [folder / name for name in data["reference_files"]]
    urls = [client.upload(path) for path in references]
    identity_video = references[0].suffix in (".mp4", ".mov", ".webm")
    videos = [prepared_url] + ([urls[0]] if identity_video else [])
    images = urls[1:] if identity_video else urls
    prompt = generation_prompt(
        data["prompt"], identity_video=identity_video, second_reference=len(references) > 1, mode=data["mode"]
    )
    if len(prompt) > 1500:
        raise ValueError("prompt_too_long")
    payload = {
        "model": "seedance-2.5", "prompt": prompt, "resolution": data["resolution"],
        "duration": max(4, min(30, round(data["duration"]))), "ratio": data["ratio"],
        "videos": videos, "generateAudio": False,
    }
    if images:
        payload["images"] = images
    update(ident, stage="submitting")
    write_json(folder / "submission.json", {"attempted_at": datetime.now(timezone.utc).isoformat()})
    try:
        task_id = client.submit(payload)
    except ProviderError:
        (folder / "submission.json").unlink(missing_ok=True)
        raise
    write_json(folder / "generation.json", {"task_id": task_id, "resolution": data["resolution"], "prompt": prompt})
    update(ident, task_id=task_id, state="generating", stage="generate")
    collect(ident)


def collect(ident):
    folder = folder_for(ident)
    data = read_job(ident)
    task_id = data.get("task_id")
    if not task_id and (folder / "generation.json").exists():
        task_id = json.loads((folder / "generation.json").read_text())["task_id"]
    if not task_id:
        raise ValueError("no_saved_task")
    client = DreamAPI(credential("DREAMAPI_API_KEY"))
    update(ident, state="generating", stage="generate", error=None, task_id=task_id)
    deadline = time.monotonic() + 3600
    transport_errors = 0
    while time.monotonic() < deadline and not STOP.is_set():
        try:
            result = client.query(task_id)
            transport_errors = 0
        except (requests.RequestException, ProviderError):
            transport_errors += 1
            if transport_errors > 3:
                raise
            STOP.wait(5)
            continue
        task = result.get("task", {})
        if task.get("status") == 4:
            raise ProviderError("Generation failed", task.get("errorCode"))
        if task.get("status") == 3:
            videos = result.get("videos", [])
            if not videos or not videos[0].get("videoUrl"):
                raise ProviderError("Result URL missing")
            update(ident, stage="restore")
            client.download(videos[0]["videoUrl"], folder / "seedance-result.mp4")
            from audio_workflow import finish_preview
            finish_preview(folder / "seedance-result.mp4", folder)
            adjusted = (folder / "duration-adjustment.json").exists()
            update(ident, state="done", stage="done", error=None, duration_adjusted=adjusted)
            return
        STOP.wait(5)
    if not STOP.is_set():
        raise TimeoutError("collection_timeout")


def recover():
    for item in list_jobs():
        ident = item["id"]
        data = read_job(ident)
        folder = folder_for(ident)
        if data["state"] in ("generating", "submitting") or (
            data["state"] == "error" and (data.get("task_id") or (folder / "generation.json").exists())
        ):
            if data.get("task_id") or (folder / "generation.json").exists():
                start_worker(ident, lambda ident=ident: collect(ident))
            elif (folder / "submission.json").exists():
                update(ident, state="uncertain", error="submission_uncertain")
            else:
                update(ident, state="review", stage="review")
        elif data["state"] in ("preparing", "repairing"):
            update(ident, state="interrupted", error="preparation_interrupted")
