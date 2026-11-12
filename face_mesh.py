"""Optional isolated face tracking. Vocal processing stays in the main runtime."""
import json
from pathlib import Path
import shutil
import subprocess
from platform_runtime import venv_python

ROOT = Path(__file__).resolve().parent


def track(folder, *, combined=False):
    from pipeline import normalize
    folder = Path(folder)
    interpreter = venv_python(ROOT / ".venv-face")
    if not interpreter.is_file():
        raise ValueError("Install the face mesh worker with setup-face-mesh.sh (macOS) or setup-face-mesh.cmd (Windows)")
    command = [str(interpreter), str(ROOT / "mesh_worker.py"), str(folder)]
    if combined:
        command.append("--depth")
    subprocess.run(command, check=True)
    # Re-encode the isolated worker's intermediate as H.264 with the main PyAV runtime.
    normalize(folder / "face-mesh-preview.mp4", folder / "composite-silent.mp4")


def run(src, folder, status=print):
    from pipeline import normalize
    from audio_workflow import separate, prepare_seedance_video
    folder = Path(folder)
    folder.mkdir(parents=True, exist_ok=True)
    status("Normalizing video")
    normalize(src, folder / "original.mp4")
    status("Tracking face mesh locally")
    track(folder)
    (folder / "workflow-mode.json").write_text(json.dumps({"mode": "face_mesh"}))
    separate(src, folder, status)
    prepare_seedance_video(folder)
    status("Face mesh ready")


def run_depth(src, folder, prompt="person", provider="replicate", status=print):
    from pipeline import run as prepare_depth
    from audio_workflow import prepare_seedance_video
    folder = Path(folder)
    prepare_depth(src, folder, prompt, provider, status)
    shutil.copy2(folder / "composite-silent.mp4", folder / "depth-composite-silent.mp4")
    status("Adding face mesh to depth guidance")
    track(folder, combined=True)
    (folder / "workflow-mode.json").write_text(json.dumps({"mode": "depth_mesh"}))
    prepare_seedance_video(folder)
    status("Depth and face mesh ready")
