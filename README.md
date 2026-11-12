# Genjustsu Pro

**English** · [简体中文](README.zh-CN.md)

A local macOS workspace for video character replacement. Prepare depth/mask or face-mesh motion guidance, inspect it, generate once with **DreamAPI Seedance 2.5**, then export with the original soundtrack.

## Features

- Day/night appearances with saved preference and a PC-first, single-screen Studio: a large viewer, internally scrolling inspector, anchored generation controls and on-demand processing steps.
- Early format, size and duration validation, inline upload requirements and dismissible, bilingual error/success toasts.
- Chinese and English interface, recent tasks, and original / guidance / depth / mask / result previews.
- Three preparation methods: Depth + SAM, Fast Face Mesh, and Depth + SAM + Face Mesh.
- DreamAPI generation and media uploads, with direct 480p / 720p / 1080p output.
- Replicate vocal separation, video depth estimation and per-frame subject segmentation.
- API keys entered on the page and saved in **macOS Keychain**, then loaded automatically on restart.
- Input approval bound to file fingerprints. Saved task IDs allow result collection to resume.
- Complete preservation of the source video's first audio track. Small duration differences are aligned using the generated video's tail and disclosed in the interface.

The language switch changes interface labels only. Model instructions retain the original upstream wording. User-entered and saved prompts are not translated when switching languages.

## Install

Requires macOS, Python 3.12+, and Rubber Band. The optional mesh worker uses Python 3.12.

```bash
git clone https://github.com/Hy-1990/Genjustsu-Pro.git
cd Genjustsu-Pro
brew install python@3.12 rubberband
PYTHON=python3.12 bash setup.sh
FACE_PYTHON=python3.12 bash setup-face-mesh.sh
```

The main environment and mesh worker are isolated. Installing the mesh worker enables both face-mesh methods. Its Google Face Landmarker model downloads at first use.

## Start

```bash
cd Genjustsu-Pro
bash start.command
```

Open **http://127.0.0.1:8771**. To use another port:

```bash
PORT=8772 bash start.command
```

Stop with **Ctrl+C**. Keep the local process running while processing. Closing the browser is fine; reopening a saved task retrieves its current state.

## First run

1. Open **API keys**.
2. Save your [DreamAPI key](https://api.newportai.com/) and [Replicate token](https://replicate.com/account/api-tokens). macOS may ask you to allow Python to access Keychain.
3. Add a **4–30 second source video with audio** (MP4/MOV/WebM, ≤500 MB) and a character reference (≤100 MB). The page checks format, size and readable duration before upload; the server checks the required audio track before starting paid preparation. Start with a single centered speaker.
4. Choose a guidance method and click **Prepare guidance**. This calls Replicate and incurs charges.
5. Inspect the entire guidance video. Approve it after checking hair, hands, clothing, background spill and face tracking. Depth methods can re-segment from the original footage, which makes another paid Replicate call.
6. Select resolution, review the prompt and click **Generate finished video**. This directly submits a paid DreamAPI generation.
7. Review and download the result. Original audio is restored locally.

Keys are stored in this Mac's Keychain. They are not stored in browser storage or returned by the server. Saving a key does not check the account balance or submit a paid generation.

## Limits and recovery

- Local single-user app, bound to localhost. One instance per project directory.
- Source upload limit 500 MB; each reference limit 100 MB. Reference images are PNG/JPEG/WebP. The primary reference may also be an MP4/MOV/WebM identity video.
- Identity reference videos can be 2–30 seconds; combined source and identity reference duration must be <=30 seconds, following the current DreamAPI reference-video limit.
- Source codecs must be decodable by PyAV and playable in the browser. Audio must be compatible with MP4 remuxing. H.264 + AAC in MP4 is the most portable input.
- Face-mesh methods target a single centered speaker. Full-clip visual approval is still required.
- The generation adapter follows the DreamAPI skill's current Seedance 2.5 multimodal input contract. Real-person reference support was confirmed by the platform owner. Output quality depends on the provider and inputs.
- Small output/source duration differences up to 1.1 seconds are aligned locally. Larger mismatches stop export rather than cutting the original soundtrack.
- If submission times out without a task ID, the interface blocks repeat submission. Check DreamAPI's task history and billing before deliberately creating another task.
- Preparation saves Replicate prediction IDs and completed artifacts. **Continue preparation** reconnects to the same cloud tasks and reuses completed steps after a local interruption. A fresh paid retry is offered only for a confirmed failed/canceled stage and requires an explicit click. An ambiguous submission blocks resubmission until provider history is checked.
- Original-footage mask repair preserves existing depth-mask coverage and fills enclosed holes locally. Inspect the full repaired guidance before approving it.
- Saved DreamAPI task IDs resume result collection; there is no automatic paid re-submission.
- Media and task metadata remain in `runs/` on this Mac. Uploaded source derivatives and references are processed by Replicate/DreamAPI and their storage providers.

## Offline checks

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python test_composite.py
.venv-face/bin/python -c "import mediapipe, cv2, PIL, numpy"
```

Tests use isolated jobs and mocked providers. They verify secret handling, review invalidation, submission contracts, ambiguous submissions, collection recovery, source-audio packet preservation and duration alignment. They do not submit paid generations.

The initial release was locally checked on macOS ARM64, Python 3.14.3 with a Python 3.12 mesh worker. A live 29.9-second Depth + SAM / image-reference / 720p workflow has also been verified through generation, original-audio restoration, playback, download and same-task restart recovery; see [verification details](docs/verification.md). Other media, modes and resolutions still need their own quality checks.

## Attribution and license

Derived from [Sirio Berati's Genjustsu Open Source Workflow](https://github.com/sirioberati/Genjustsu-Open-Source-Workflow) at commit `40fd6615c2b7d940d4d7060e82de522292eefe99`. Upstream code remains under its [MIT license](LICENSE). Upstream example videos, names, logos and companion artwork are excluded from that grant and are not distributed here.

See [THIRD-PARTY.md](THIRD-PARTY.md) for dependency and hosted-model notices.
