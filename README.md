# Genjustsu Pro

A local macOS workspace for video character replacement. Prepare depth/mask or face-mesh motion guidance, inspect it, generate once with **DreamAPI Seedance 2.5**, then export with the original soundtrack.

一个本地运行的视频换角工作台。先准备并检查动作引导，再通过 **DreamAPI Seedance 2.5** 直接生成所选分辨率，导出时恢复原始音轨。

## 功能 / Features

- 中文、英文切换，最近任务与原片 / 引导 / 深度 / 遮罩 / 成片预览。
- 三种引导方式：Depth + SAM、Fast Face Mesh、Depth + SAM + Face Mesh。
- DreamAPI 生成与素材上传，直接输出 480p / 720p / 1080p。
- Replicate 完成人声分离、视频深度估计和逐帧人物分割。
- 页面配置 API 密钥，使用 **macOS Keychain** 保存，重启后自动读取。
- 输入审批绑定文件指纹。记录生成任务 ID，重启后继续获取结果。
- 完整保留源视频第一条音轨。生成时长取整产生的小幅偏差，会通过生成画面尾部补帧或裁剪对齐，并在页面提示。

Bilingual workspace, three preparation modes, Keychain credentials, single-pass generation, review gates, saved job recovery and original-audio restoration.

## 安装 / Install

Requires macOS, Python 3.12+, and Rubber Band. The optional mesh worker uses Python 3.12.

```bash
git clone https://github.com/Hy-1990/Genjustsu-Pro.git
cd Genjustsu-Pro
brew install python@3.12 rubberband
PYTHON=python3.12 bash setup.sh
FACE_PYTHON=python3.12 bash setup-face-mesh.sh
```

The main environment and mesh worker are isolated. Installing the mesh worker enables both face-mesh modes. Its Google Face Landmarker model downloads at first use.

## 启动 / Start

```bash
cd Genjustsu-Pro
bash start.command
```

Open **http://127.0.0.1:8771**. To use another port:

```bash
PORT=8772 bash start.command
```

Stop with **Ctrl+C**. Keep the local process running while processing. Closing the browser is fine; reopening a saved task retrieves its current state.

## 首次使用 / First run

1. Open **密钥设置 / API keys**.
2. Save your [DreamAPI key](https://api.newportai.com/) and [Replicate token](https://replicate.com/account/api-tokens). macOS may ask you to allow Python to access Keychain.
3. Add a **4–30 second source video with audio** and a character reference. Start with a single centered speaker.
4. Choose a guidance method and click **准备引导视频 / Prepare guidance**. This calls Replicate and incurs charges.
5. Inspect the entire guidance video. Approve it after checking hair, hands, clothing, background spill and face tracking. Depth modes can re-segment from the original footage, which makes another paid Replicate call.
6. Select resolution, review the prompt and click **生成完整视频 / Generate finished video**. This directly submits a paid DreamAPI generation.
7. Review and download the result. Original audio is restored locally.

密钥只写入当前 Mac 的钥匙串。浏览器不保存密钥，服务端不通过接口返回密钥内容。保存密钥不会验证余额或发起付费生成。

## 约束与恢复 / Limits and recovery

- Local single-user app, bound to localhost. One instance per project directory.
- Source upload limit 500 MB; each reference limit 100 MB. Reference images are PNG/JPEG/WebP. The primary reference may also be an MP4/MOV/WebM identity video.
- Identity reference videos can be 2–30 seconds; combined source and identity reference duration must be <=30 seconds, following the current DreamAPI reference-video limit.
- Source codecs must be decodable by PyAV and playable in the browser. Audio must be compatible with MP4 remuxing. H.264 + AAC in MP4 is the most portable input.
- Face-mesh modes target a single centered speaker. Full-clip visual approval is still required.
- The generation adapter follows the DreamAPI skill's current Seedance 2.5 multimodal input contract. Real-person reference support was confirmed by the platform owner. Output quality depends on the provider and inputs.
- Small output/source duration differences up to 1.1 seconds are aligned locally. Larger mismatches stop export rather than cutting the original soundtrack.
- If submission times out without a task ID, the UI blocks repeat submission. Check DreamAPI's task history and billing before deliberately creating another task.
- Saved task IDs resume collection; there is no automatic paid re-submission. After a preparation interruption, check Replicate's task history before repeating preparation.
- Media and task metadata remain in `runs/` on this Mac. Uploaded source derivatives and references are processed by Replicate/DreamAPI and their storage providers.

## 本地验证 / Offline checks

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python test_composite.py
.venv-face/bin/python -c "import mediapipe, cv2, PIL, numpy"
```

Tests use isolated jobs and mocked providers. They verify secret handling, review invalidation, submission contracts, ambiguous submissions, collection recovery, source-audio packet preservation and duration alignment. They do not submit paid generations.

The initial release was locally checked on macOS ARM64, Python 3.14.3 with a Python 3.12 mesh worker. Live cloud generation and account billing require your own test.

## 来源与许可 / Attribution and license

Derived from [Sirio Berati's Genjustsu Open Source Workflow](https://github.com/sirioberati/Genjustsu-Open-Source-Workflow) at commit `40fd6615c2b7d940d4d7060e82de522292eefe99`. Upstream code remains under its [MIT license](LICENSE). Upstream example videos, names, logos and companion artwork are excluded from that grant and are not distributed here.

See [THIRD-PARTY.md](THIRD-PARTY.md) for dependency and hosted-model notices.
