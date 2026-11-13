# Third-party components

Video/audio preprocessing, mask review and mesh logic derive from Sirio Berati's MIT-licensed Genjustsu workflow, commit 40fd6615c2b7d940d4d7060e82de522292eefe99. Original copyright and permission notice are retained in LICENSE.

This application uses FastAPI, Uvicorn, PyAV, NumPy, Pillow, Requests, OpenCV, SciPy, Gradio Client, keyring and optional MediaPipe. Each component retains its own license.

Rubber Band is installed separately. MediaPipe Face Landmarker weights are fetched from Google's model hosting on first use and retain their model terms.

Replicate hosts Demucs htdemucs, Depth Anything video and SAM 3 models. Those services and model weights retain their provider and model licenses.

DreamAPI provides Seedance 2.5 and media storage. Service availability, real-person reference handling, billing and generated media use remain subject to provider and model terms.

No upstream demonstration footage or TEIN brand assets are included.

## Manrope heading font

The locally hosted Manrope variable font is distributed under the SIL Open Font License 1.1. Source: [Google Fonts](https://fonts.google.com/specimen/Manrope), [google/fonts repository](https://github.com/google/fonts/tree/main/ofl/manrope). The complete license is included at `static/fonts/OFL-Manrope.txt`. Native platform fonts remain the body and Chinese fallback fonts.

Public demo source, character reference and replacement videos were generated for Henge using DreamAPI. The promotional clips show actual Henge workflow output and contain no upstream example media.
