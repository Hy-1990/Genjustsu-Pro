# Genjustsu Pro

[English](README.md) · **简体中文**

一个本地运行的视频换角工作台。先准备并检查动作引导，再通过 **DreamAPI Seedance 2.5** 直接生成所选分辨率，导出时恢复原始音轨。

## 功能

- 深色工作台，固定展示真实执行步骤、运行状态、错误和恢复入口。
- 中文、英文界面切换，最近任务与原片、引导、深度、遮罩、成片预览。
- 三种引导方式：深度 + SAM 人物分割、人脸网格、深度 + SAM 人物分割 + 人脸网格。
- 使用 DreamAPI 生成视频和上传素材，直接输出 480p、720p 或 1080p。
- 使用 Replicate 完成人声分离、视频深度估计和逐帧人物分割。
- 页面配置 API 密钥，使用 **macOS 系统钥匙串**保存，重启后自动读取。
- 输入审批绑定文件指纹。记录生成任务编号，重启后继续获取结果。
- 完整保留源视频第一条音轨。生成时长取整产生的小幅偏差，会通过生成画面尾部补帧或裁剪对齐，并在页面提示。

语言切换只影响界面文案。模型提示词保留原项目的原文；切换界面语言时，不会翻译用户填写或任务已保存的提示词。

## 安装

需要 macOS、Python 3.12 及以上版本和 Rubber Band。可选的人脸网格组件使用 Python 3.12。

```bash
git clone https://github.com/Hy-1990/Genjustsu-Pro.git
cd Genjustsu-Pro
brew install python@3.12 rubberband
PYTHON=python3.12 bash setup.sh
FACE_PYTHON=python3.12 bash setup-face-mesh.sh
```

主程序与人脸网格组件使用独立环境。安装网格组件后，两种带人脸网格的引导方式均可使用。首次使用时会下载 Google Face Landmarker 模型。

## 启动

```bash
cd Genjustsu-Pro
bash start.command
```

打开 **http://127.0.0.1:8771**。如需更换端口：

```bash
PORT=8772 bash start.command
```

按 **Ctrl+C** 停止应用。处理期间保持本地程序运行。可以关闭浏览器，重新打开已保存的任务后会显示当前进度。

## 首次使用

1. 打开**密钥设置**。
2. 保存你的 [DreamAPI 密钥](https://api.newportai.com/)和 [Replicate 密钥](https://replicate.com/account/api-tokens)。macOS 可能询问是否允许 Python 访问钥匙串。
3. 添加一段**带原声的 4–30 秒视频**和目标角色参考。建议先用单人居中口播。
4. 选择引导方式，点击**准备引导视频**。此步骤会调用 Replicate 并产生费用。
5. 检查整段引导视频，确认头发、手、服装、背景遮罩和人脸跟踪正确后批准。深度模式可以使用原片重新分割，此操作会再次调用 Replicate 并计费。
6. 选择分辨率、检查提示词，点击**生成完整视频**。此步骤会直接提交 DreamAPI 付费生成任务。
7. 检查并下载成片，程序会在本地恢复原始音轨。

密钥只写入当前 Mac 的系统钥匙串。浏览器不保存密钥，服务端不通过接口返回密钥内容。保存密钥不会验证余额或发起付费生成。

## 使用限制与恢复

- 本地单用户应用，仅监听本机地址。同一个项目目录同时运行一个实例。
- 原视频上限为 500 MB，每份参考上限为 100 MB。支持 PNG、JPEG、WebP 参考图，主角色也可以使用 MP4、MOV 或 WebM 身份参考视频。
- 身份参考视频为 2–30 秒；按当前 DreamAPI 视频参考限制，原片与身份参考视频的时长总和不能超过 30 秒。
- 源视频需要能被 PyAV 解码并在浏览器中播放，音轨需要支持封装到 MP4。H.264 视频和 AAC 音轨的 MP4 兼容性最好。
- 人脸网格适合单人居中口播，仍需检查并批准整段引导。
- 生成适配器按照 DreamAPI 技能文档中的 Seedance 2.5 多模态输入协议实现。平台所有者已确认支持真人参考，实际效果取决于模型和素材。
- 生成视频与原片不超过 1.1 秒的时长差会在本地对齐。更大的偏差会停止导出，保留原始音轨。
- 提交超时且没有返回任务编号时，界面会阻止重复提交。请先在 DreamAPI 核对任务和计费记录，再决定是否新建任务。
- 预处理会保存 Replicate 任务编号与已完成文件。本地中断后，点击**继续准备引导**会继续获取同一任务并复用已完成步骤；只有确认失败或取消的步骤才提供付费重试入口，需明确点击。提交结果不明时会阻止再次提交，避免重复计费。
- 原片遮罩修复会保留已有深度遮罩的覆盖范围，并在本地补齐内部孔洞；修复后仍需检查整段引导再批准。
- DreamAPI 任务编号可用于继续获取结果，不会自动重新提交付费生成。
- 视频和任务记录保留在当前 Mac 的 `runs/` 目录。上传的处理素材和参考图会交由 Replicate、DreamAPI 及其存储服务处理。

## 本地验证

```bash
.venv/bin/python -m unittest discover -s tests -v
.venv/bin/python test_composite.py
.venv-face/bin/python -c "import mediapipe, cv2, PIL, numpy"
```

测试使用独立任务目录和模拟云端服务，验证密钥处理、审批失效、提交协议、不确定提交、结果恢复、原始音轨数据包保留和时长对齐，不会提交付费生成。

初版已在 macOS ARM64、Python 3.14.3 和 Python 3.12 人脸网格环境中完成本地验证。另已通过一次 29.9 秒、深度 + SAM、图片身份参考、720p 的真实云端测试，验证生成、原声恢复、播放、下载和重启后继续同一任务；见[验证记录](docs/verification.md)。其他素材、模式与分辨率仍需分别验证效果。

## 来源与许可

基于 [Sirio Berati 的 Genjustsu 开源工作流](https://github.com/sirioberati/Genjustsu-Open-Source-Workflow)，对应提交 `40fd6615c2b7d940d4d7060e82de522292eefe99`。上游代码保留其 [MIT 许可](LICENSE)。上游示例视频、名称、标志和配套品牌插图不在该许可授权范围内，本项目不包含这些资产。

第三方依赖和托管模型说明见 [THIRD-PARTY.md](THIRD-PARTY.md)。
