"""Isolated MediaPipe tracking worker. OpenCV handles video I/O in this process."""
import json
from pathlib import Path
import sys
import urllib.request

import cv2
import mediapipe as mp
import numpy as np
from PIL import Image, ImageDraw

root = Path(sys.argv[1]).resolve()
model = Path(__file__).resolve().parent / "models/face_landmarker.task"
if not model.exists():
    model.parent.mkdir(exist_ok=True)
    temporary = model.with_suffix(".download")
    urllib.request.urlretrieve(
        "https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/latest/face_landmarker.task",
        str(temporary),
    )
    temporary.replace(model)

options = mp.tasks.vision.FaceLandmarkerOptions(
    base_options=mp.tasks.BaseOptions(model_asset_path=str(model)),
    running_mode=mp.tasks.vision.RunningMode.VIDEO,
    num_faces=1,
    min_face_detection_confidence=0.15,
    min_face_presence_confidence=0.15,
    min_tracking_confidence=0.15,
)
connections = mp.tasks.vision.FaceLandmarksConnections
source = cv2.VideoCapture(str(root / "original.mp4"))
background = cv2.VideoCapture(str(root / "depth-composite-silent.mp4")) if "--depth" in sys.argv else None
if not source.isOpened() or (background is not None and not background.isOpened()):
    raise ValueError("Unable to open normalized video")

width, height = int(source.get(cv2.CAP_PROP_FRAME_WIDTH)), int(source.get(cv2.CAP_PROP_FRAME_HEIGHT))
writer = cv2.VideoWriter(str(root / "face-mesh-preview.mp4"), cv2.VideoWriter_fourcc(*"mp4v"), 24, (width, height))
if not writer.isOpened():
    raise ValueError("Unable to encode face mesh video")

saved = []
missing = []
index = 0
try:
    with mp.tasks.vision.FaceLandmarker.create_from_options(options) as detector:
        while True:
            available, frame = source.read()
            if not available:
                break
            original = Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            x0, crop_width, crop_height = int(width * 0.25), int(width * 0.5), int(height * 0.65)
            crop = original.crop((x0, 0, x0 + crop_width, crop_height))
            result = detector.detect_for_video(
                mp.Image(image_format=mp.ImageFormat.SRGB, data=np.array(crop)),
                round(index * 1000 / 24),
            )
            image = original
            if background is not None:
                background_ok, bg_frame = background.read()
                if not background_ok or bg_frame.shape[:2] != (height, width):
                    raise ValueError("Depth and original frames are misaligned")
                image = Image.fromarray(cv2.cvtColor(bg_frame, cv2.COLOR_BGR2RGB))
            draw = ImageDraw.Draw(image)
            saved.append({
                "frame": index,
                "time": index / 24,
                "faces": [[{"x": (x0 + point.x * crop_width) / width, "y": point.y * crop_height / height}
                           for point in face] for face in result.face_landmarks],
            })
            if not result.face_landmarks:
                missing.append(index)
            for face in result.face_landmarks:
                points = [(round(x0 + point.x * crop_width), round(point.y * crop_height)) for point in face]
                for edge in connections.FACE_LANDMARKS_TESSELATION:
                    draw.line([points[edge.start], points[edge.end]], fill=(50, 170, 205), width=1)
                for name, color in (
                    ("FACE_LANDMARKS_LIPS", (255, 135, 100)),
                    ("FACE_LANDMARKS_LEFT_EYE", (130, 255, 150)),
                    ("FACE_LANDMARKS_RIGHT_EYE", (130, 255, 150)),
                ):
                    for edge in getattr(connections, name):
                        draw.line([points[edge.start], points[edge.end]], fill=color, width=2)
            writer.write(cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR))
            index += 1
        if background is not None and background.read()[0]:
            raise ValueError("Depth contains additional frames")
finally:
    source.release()
    writer.release()
    if background is not None:
        background.release()

(root / "face-landmarks.json").write_text(json.dumps({"fps": 24, "frames": saved}))
tracking = {"frames": index, "tracked": index - len(missing), "missing_frames": missing}
(root / "face-tracking.json").write_text(json.dumps(tracking))
print(tracking)
if not index or missing:
    raise RuntimeError("Face tracking gaps: inspect the entire clip before generating")
