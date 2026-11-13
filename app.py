"""Local-only Henge browser application."""
from contextlib import asynccontextmanager
from pathlib import Path
import secrets
import shutil
import threading
import uuid

from fastapi import FastAPI, File, Form, HTTPException, Request, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

import credential_store
import jobs
from config import ROOT
from platform_runtime import venv_python, lock_runtime, unlock_runtime
from mask_review import review, require_approved

TOKEN = secrets.token_urlsafe(32)
mutation_lock = threading.RLock()


@asynccontextmanager
async def lifespan(app):
    lockfile = (jobs.RUNS / ".runtime.lock").open("a+b")
    try:
        lock_runtime(lockfile)
    except OSError:
        lockfile.close()
        raise RuntimeError("Henge is already running from this project.")
    try:
        jobs.STOP.clear()
        jobs.recover()
        yield
    finally:
        jobs.STOP.set()
        unlock_runtime(lockfile)
        lockfile.close()


app = FastAPI(title="Henge", lifespan=lifespan, docs_url=None, redoc_url=None)


@app.middleware("http")
async def local_access(request: Request, call_next):
    host = request.url.hostname
    if host not in ("127.0.0.1", "localhost", "testserver"):
        return JSONResponse({"detail": "local_only"}, status_code=403)
    origin = request.headers.get("origin")
    if origin and origin != str(request.base_url).rstrip("/"):
        return JSONResponse({"detail": "invalid_origin"}, status_code=403)
    if request.method not in ("GET", "HEAD", "OPTIONS"):
        if not secrets.compare_digest(request.headers.get("x-local-token", ""), TOKEN):
            return JSONResponse({"detail": "invalid_session"}, status_code=403)
    response = await call_next(request)
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "no-referrer"
    response.headers["X-Frame-Options"] = "DENY"
    if request.url.path.startswith(("/api/", "/static/")):
        response.headers["Cache-Control"] = "no-store"
    return response


@app.exception_handler(FileNotFoundError)
async def missing_file(request, exc):
    return JSONResponse({"detail": "job_not_found"}, status_code=404)


@app.exception_handler(ValueError)
async def bad_input(request, exc):
    known = {"job_busy", "duration_range", "audio_required", "invalid_video",
             "mesh_no_mask", "prompt_too_long", "no_saved_task"}
    detail = str(exc) if str(exc) in known else "invalid_input"
    return JSONResponse({"detail": detail}, status_code=400)


@app.get("/")
def index():
    return FileResponse(ROOT / "static/index.html", headers={"Cache-Control": "no-store"})


@app.get("/api/session")
def session():
    return {"token": TOKEN}


@app.get("/health")
def health():
    return {"status": "ok", "service": "Henge"}


@app.get("/api/keys")
def get_keys():
    try:
        return {"providers": credential_store.key_status()}
    except Exception:
        raise HTTPException(503, "keychain_unavailable") from None


class KeyInput(BaseModel):
    value: str = Field(min_length=1, max_length=4096)


@app.put("/api/keys/{provider}")
def set_key(provider: str, data: KeyInput):
    if provider not in credential_store.PROVIDERS:
        raise HTTPException(404, "unknown_provider")
    try:
        credential_store.save_key(provider, data.value)
    except ValueError:
        raise HTTPException(400, "invalid_key") from None
    except Exception:
        raise HTTPException(503, "keychain_unavailable") from None
    return {"configured": True}


@app.delete("/api/keys/{provider}")
def remove_key(provider: str):
    if provider not in credential_store.PROVIDERS:
        raise HTTPException(404, "unknown_provider")
    try:
        credential_store.delete_key(provider)
    except Exception:
        raise HTTPException(503, "keychain_unavailable") from None
    return {"configured": False}


def require_key(provider):
    try:
        value = credential_store.get_key(provider)
    except Exception:
        raise HTTPException(503, "keychain_unavailable") from None
    if not value:
        raise HTTPException(400, "keys_required")


def save_upload(upload, target, limit=500_000_000):
    size = 0
    with target.open("wb") as output:
        while chunk := upload.file.read(1024 * 1024):
            size += len(chunk)
            if size > limit:
                target.unlink(missing_ok=True)
                raise HTTPException(413, "file_too_large")
            output.write(chunk)
    if not size:
        target.unlink(missing_ok=True)
        raise HTTPException(400, "empty_file")


@app.get("/api/jobs")
def get_jobs():
    return jobs.list_jobs()


@app.post("/api/jobs", status_code=201)
def create_job(video: UploadFile = File(...), mode: str = Form("depth"), subject: str = Form("person")):
    require_key("replicate")
    if mode not in jobs.MODES or not subject.strip() or len(subject) > 200:
        raise HTTPException(400, "invalid_input")
    suffix = Path(video.filename or "").suffix.lower()
    if suffix not in (".mp4", ".mov", ".webm"):
        raise HTTPException(400, "invalid_video")
    if mode != "depth" and not venv_python(ROOT / ".venv-face").is_file():
        raise HTTPException(400, "mesh_unavailable")
    ident = uuid.uuid4().hex
    folder = jobs.RUNS / ident
    folder.mkdir(mode=0o700)
    try:
        save_upload(video, folder / "upload.mp4")
        try:
            metadata = jobs.inspect_video(folder / "upload.mp4", source=True)
        except ValueError:
            raise
        except Exception:
            raise ValueError("invalid_video") from None
        data = {
            "id": ident, "name": Path(video.filename).name, "mode": mode,
            "subject": subject.strip(), **metadata, "created_at": jobs.datetime.now(jobs.timezone.utc).isoformat(),
            "state": "preparing", "stage": "prepare", "error": None,
        }
        jobs.write_json(folder / "job.json", data)
    except Exception:
        shutil.rmtree(folder)
        raise
    jobs.start_worker(ident, lambda: jobs.prepare(ident))
    return {"id": ident}


@app.get("/api/jobs/{ident}")
def get_job(ident: str):
    return jobs.public_job(ident)


class ReviewInput(BaseModel):
    approved: bool
    fingerprint: str


@app.post("/api/jobs/{ident}/review")
def approve_input(ident: str, data: ReviewInput):
    with mutation_lock:
        job = jobs.read_job(ident)
        if job["state"] not in ("review", "ready"):
            raise HTTPException(409, "job_busy")
        try:
            result = review(jobs.folder_for(ident), data.approved, "Reviewed by user", data.fingerprint)
        except ValueError:
            raise HTTPException(409, "review_changed") from None
        jobs.update(ident, state="ready" if data.approved else "review", stage="review")
        return {"approved": result["approved"]}


@app.post("/api/jobs/{ident}/repair")
def repair_input(ident: str):
    require_key("replicate")
    with mutation_lock:
        data = jobs.read_job(ident)
        if data["mode"] == "face_mesh":
            raise HTTPException(400, "mesh_no_mask")
        if data["state"] not in ("review", "ready") or (jobs.folder_for(ident) / "submission.json").exists():
            raise HTTPException(409, "job_busy")
        jobs.update(ident, state="repairing", stage="mask", error=None, preparation_action="repair")
        jobs.start_worker(ident, lambda: jobs.repair(ident))
    return {"state": "repairing"}


@app.post("/api/jobs/{ident}/generate")
def generate(
    ident: str, prompt: str = Form(...), resolution: str = Form("720p"),
    reference: UploadFile = File(...), second_reference: UploadFile | None = File(None),
):
    require_key("dreamapi")
    if resolution not in ("480p", "720p", "1080p") or not prompt.strip() or len(prompt.strip()) > 950:
        raise HTTPException(400, "invalid_input")
    folder = jobs.folder_for(ident)
    with mutation_lock:
        data = jobs.read_job(ident)
        if data["state"] not in ("ready", "error"):
            raise HTTPException(409, "job_busy")
        if (folder / "submission.json").exists() or (folder / "generation.json").exists():
            raise HTTPException(409, "already_submitted")
        try:
            require_approved(folder)
        except ValueError:
            raise HTTPException(409, "review_required") from None
        references = []
        for number, upload in enumerate((reference, second_reference), 1):
            if upload is None or not upload.filename:
                continue
            suffix = Path(upload.filename).suffix.lower()
            allowed = (".png", ".jpg", ".jpeg", ".webp")
            if number == 1:
                allowed += (".mp4", ".mov", ".webm")
            if suffix not in allowed:
                raise HTTPException(400, "invalid_reference")
            target = folder / f"reference-{number}{suffix}"
            save_upload(upload, target, limit=100_000_000)
            if suffix in (".mp4", ".mov", ".webm"):
                meta = jobs.inspect_video(target)
                if meta["duration"] + data["duration"] > 30:
                    target.unlink(missing_ok=True)
                    raise HTTPException(400, "reference_duration")
            else:
                from PIL import Image
                try:
                    with Image.open(target) as image:
                        image.verify()
                except Exception:
                    target.unlink(missing_ok=True)
                    raise HTTPException(400, "invalid_reference") from None
            references.append(target.name)
        ratios = {"16:9": 16/9, "9:16": 9/16, "1:1": 1, "4:3": 4/3, "3:4": 3/4, "21:9": 21/9}
        ratio = min(ratios, key=lambda value: abs(ratios[value] - data["width"] / data["height"]))
        jobs.update(ident, prompt=prompt.strip(), resolution=resolution, ratio=ratio,
                    reference_files=references, state="submitting", stage="upload", error=None)
        jobs.start_worker(ident, lambda: jobs.generate(ident))
    return {"state": "submitting"}


@app.post("/api/jobs/{ident}/retry-preparation")
def retry_preparation(ident: str):
    require_key("replicate")
    with mutation_lock:
        data = jobs.public_job(ident)
        stage = data["retry_preparation_stage"]
        if not stage or data["task_submitted"] or not data["can_resume_preparation"]:
            raise HTTPException(409, "job_busy")
        folder = jobs.folder_for(ident)
        from replicate_jobs import get_response, read_prediction, save_prediction
        from config import credential
        path = jobs.preparation_prediction_path(folder, data, stage)
        saved = read_prediction(path)
        latest = get_response(saved["urls"]["get"], {"Authorization": "Bearer " + credential("REPLICATE_API_TOKEN")}).json()
        save_prediction(path, latest)
        if latest.get("status") not in ("failed", "canceled"):
            raise HTTPException(409, "job_busy")
        archive = folder / "attempts"
        archive.mkdir(exist_ok=True)
        path.replace(archive / (path.stem + "-" + uuid.uuid4().hex + ".json"))
        state = "repairing" if data.get("preparation_action") == "repair" else "preparing"
        action = jobs.repair if state == "repairing" else jobs.prepare
        jobs.update(ident, state=state, stage="mask" if state == "repairing" else "prepare", error=None, provider_status=None)
        jobs.start_worker(ident, lambda: action(ident))
    return {"state": state}


@app.post("/api/jobs/{ident}/resume-preparation")
def resume_preparation(ident: str):
    require_key("replicate")
    with mutation_lock:
        data = jobs.public_job(ident)
        if not data["can_resume_preparation"] or data["task_submitted"]:
            raise HTTPException(409, "job_busy")
        state = "repairing" if data.get("preparation_action") == "repair" else "preparing"
        action = jobs.repair if state == "repairing" else jobs.prepare
        jobs.update(ident, state=state, stage="mask" if state == "repairing" else "prepare", error=None, provider_status=None)
        jobs.start_worker(ident, lambda: action(ident))
    return {"state": state}


@app.post("/api/jobs/{ident}/resume")
def resume(ident: str):
    require_key("dreamapi")
    with mutation_lock:
        data = jobs.read_job(ident)
        if data["state"] != "error":
            raise HTTPException(409, "job_busy")
        if not data.get("task_id") and not (jobs.folder_for(ident) / "generation.json").exists():
            raise HTTPException(400, "no_saved_task")
        jobs.update(ident, state="generating", stage="generate", error=None)
        jobs.start_worker(ident, lambda: jobs.collect(ident))
    return {"state": "generating"}


@app.get("/api/jobs/{ident}/files/{filename}")
def get_media(ident: str, filename: str):
    allowed = {"upload.mp4", "original.mp4", "depth.mp4", "mask.mp4", "seedance-input.mp4", "final-preview.mp4"}
    reference_names = {f"reference-{number}{suffix}" for number in (1, 2)
                       for suffix in (".png", ".jpg", ".jpeg", ".webp", ".mp4", ".mov", ".webm")}
    if filename not in allowed | reference_names:
        raise HTTPException(404, "file_not_found")
    target = jobs.folder_for(ident) / filename
    if not target.is_file():
        raise HTTPException(404, "file_not_found")
    return FileResponse(target, filename=filename, content_disposition_type="inline")


app.mount("/static", StaticFiles(directory=ROOT / "static"), name="static")
