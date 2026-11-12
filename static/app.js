"use strict";

// Core workflow text is independent of the interface language.
const WORKFLOW_DEFAULT_PROMPT = "Replace the complete selected subject with the supplied character reference in every frame, including hair, hands, clothing and footwear. Preserve the original background, camera framing, lighting, motion and timing. Match the embedded speech exactly without extra dialogue. Use the embedded vocals in @Video1 for performance and lip synchronization. If using two characters, specify which subject each reference replaces before submitting.";

const copy = {
  zh: {
    newTask: "新建任务", recent: "最近任务", historyEmpty: "任务会保留在这里，随时回来继续。",
    localWorkspace: "本地工作空间", workspace: "视频换角工作台", settings: "密钥设置",
    title: "视频换角工作台", subtitle: "素材准备、动作引导、角色生成，在一条可恢复的工作流里完成。",
    setupNotice: "首次使用，请先配置 DreamAPI 和 Replicate 密钥。", configure: "去配置",
    stepPrepare: "准备素材", stepReview: "检查引导", stepGenerate: "生成与导出",
    materials: "输入素材", sourceVideo: "原始视频", required: "必填", chooseVideo: "选择或拖入视频",
    sourceHint: "4–30 秒 · MP4 / MOV / WebM · 含原声", advanced: "预处理选项",
    method: "引导方式", modeDepth: "深度 + 人物分割", modeMesh: "人脸网格 · 适合居中口播",
    modeBoth: "深度 + 分割 + 人脸网格", subject: "要替换的主体",
    subjectHint: "默认 person 会选择检测到的人物。多人时请仔细检查遮罩。",
    prepare: "准备引导视频", prepareCost: "此步骤会调用 Replicate 并产生费用。",
    character: "目标角色", chooseReference: "添加角色参考", referenceHint: "图片或身份参考视频",
    addSecond: "添加第二个角色参考（可选）", chooseImage: "选择参考图片", prompt: "替换说明",
    promptHint: "描述人物如何替换。多个角色需注明与原片人物的对应关系。",
    resolution: "输出分辨率", generate: "生成完整视频", generationGate: "先准备并批准引导视频，即可生成。",
    generationCost: "将直接调用 DreamAPI 生成完整视频并计费。", preview: "视频预览",
    stateIdle: "等待素材", emptyTitle: "从一段原始视频开始",
    emptyCopy: "上传素材后，在这里对照原片、动作引导与最终结果。",
    originalAudio: "最终成片保留原始音轨", download: "下载视频",
    reviewTitle: "生成前，检查整段视频",
    reviewCopy: "确认头发、手和衣服都在遮罩内，背景没有被误选；人脸网格需全程贴合。听一下人声与动作是否同步。",
    reviewConfirm: "我已检查整段引导视频，确认可以生成。", approve: "批准引导", repair: "用原片重新分割",
    repairHint: "重新分割会额外调用 Replicate，完成后需要再次检查。",
    approved: "引导已批准，可以生成。", attention: "任务需要处理", resume: "继续获取结果",
    resultReady: "成片已就绪", resultCopy: "原始音轨已恢复。播放检查人物、动作和口型后即可下载。",
    durationNote: "已微调生成画面的尾部时长以匹配原片，原始音轨保持完整。",
    workflowNote: "预处理使用 Replicate，视频生成使用 DreamAPI。每次生成直接输出所选分辨率。",
    back: "返回工作台", settingsTitle: "连接你的模型服务",
    settingsSubtitle: "密钥保存在这台 Mac 的系统钥匙串，下次启动自动读取。",
    dreamRole: "Seedance 2.5 视频生成与素材上传", replicateRole: "人声分离、深度估计与人物分割",
    saveKey: "保存密钥", getKey: "获取密钥", removeKey: "移除已存密钥",
    keychainNote: "首次保存或读取时，macOS 可能询问钥匙串访问权限。请允许本应用的 Python 访问。页面只显示配置状态，保存后不会回显密钥。",
    keyBilling: "保存密钥仅连接账户，实际处理会按各平台用量计费。账户需要有可用额度。",
    configured: "已配置", unconfigured: "未配置", keySaved: "密钥已保存到系统钥匙串。", keyRemoved: "密钥已移除。",
    confirmRemove: "确定移除这个服务的已存密钥？", original: "原片", guidance: "动作引导", depth: "深度", mask: "遮罩", result: "成片",
    sourceLocal: "原始素材 · 尚未上传", clipSeconds: "秒", jobCreated: "已开始准备素材。",
    state_preparing: "准备中", state_repairing: "重新分割中", state_review: "待检查", state_ready: "可生成",
    state_submitting: "提交中", state_generating: "生成中", state_done: "已完成", state_error: "需处理",
    state_uncertain: "待核实", state_interrupted: "准备已中断",
    stage_prepare: "正在准备原始视频", stage_audio: "正在处理原始人声", stage_depth: "正在生成深度视频",
    stage_mask: "正在分割人物", stage_composite: "正在合成动作引导", stage_mesh: "正在追踪面部动作",
    stage_upload: "正在上传生成素材", stage_submitting: "正在提交生成任务", stage_generate: "Seedance 正在生成视频",
    stage_restore: "正在恢复原始音轨", stage_review: "等待检查引导", stage_done: "视频已就绪",
    monitorIdle: "等待输入素材", monitorIdleCopy: "配置素材后，整个处理过程会在这里实时展示。",
    monitorUploading: "正在上传原始素材", monitorUploadingCopy: "正在创建任务并读取视频，页面会自动显示后续进度。",
    monitorReview: "动作引导已就绪，等待你的检查", monitorReady: "引导已批准，可以生成",
    monitorError: "处理已暂停 · 已完成步骤已保留", monitorDone: "成片已就绪",
    step_input: "素材上传", step_audio: "人声分离", step_depth: "深度估计", step_mask: "人物分割",
    step_mesh: "面部追踪", step_composite: "引导合成", step_review: "检查批准", step_generate: "角色生成", step_restore: "原声恢复",
    stepState_waiting: "待检查", stepState_done: "已完成", stepState_active: "处理中", stepState_error: "需处理", stepState_pending: "等待",
    preparingAction: "正在准备…", generatingAction: "正在生成…",
    retryPreparation: "重试失败步骤", retryChargeConfirm: "仅重试已明确失败的当前步骤。已完成结果会复用，本次模型重试可能再次计费。继续吗？",
    resumePreparation: "继续准备引导",
    cloudQueued: "Replicate 已接受任务，正在排队或启动模型。此时请求成功不代表视频已处理完成。",
    cloudRunning: "Replicate 模型正在处理视频。时长取决于原片长度和模型运行速度。",
    error_preparation_uncertain: "预处理提交结果尚未确认。请先核对 Replicate 任务记录，确认后再决定下一步。",
    preparingCopy: "保留原片的动作与时间节奏。处理期间可以切换到其他任务。",
    generatingCopy: "通常需要数分钟。关闭页面后可重新打开任务，程序会继续获取同一结果。",
    repairingCopy: "使用原始画面细节修复遮罩，完成后请重新检查整段引导。",
    selectSource: "请先选择一段原始视频。", selectReference: "请添加目标角色参考。",
    error_provider_payment: "云端服务返回付款或额度错误（402）。请检查此阶段所用平台的计费设置与可用额度。",
    error_provider_auth: "云端服务拒绝了密钥。请在密钥设置中更新对应平台的密钥。",
    error_provider_error: "云端处理失败。请检查平台任务记录、素材要求及可用额度。",
    error_network_error: "连接云端服务失败。请检查网络；已有生成任务可点击“继续获取结果”。",
    error_collection_timeout: "等待生成结果超时。任务编号已保留，可继续获取同一任务的结果。",
    error_processing_error: "处理未完成。请检查素材是否可播放、人物是否可追踪，以及云端任务记录。",
    error_keys_required: "请先在密钥设置中配置对应平台的密钥。",
    error_submission_uncertain: "提交后未收到明确结果。请先到 DreamAPI 查看任务记录，确认是否已计费或生成。请勿直接重复提交；核实后再新建任务。",
    error_preparation_interrupted: "上次准备过程已中断。请先检查 Replicate 任务记录，再决定是否新建任务重新准备。",
    error_keychain_unavailable: "无法访问 macOS 钥匙串。请检查系统的访问授权后重试。",
    error_invalid_key: "密钥不能为空或包含空格，请检查后重新保存。",
    error_invalid_video: "无法读取视频。请选择可播放的 MP4、MOV 或 WebM 文件。",
    error_audio_required: "原视频需要包含音轨，导出时会恢复这条原始音轨。",
    error_duration_range: "原视频时长需为 4–30 秒，参考视频需为 2–30 秒。",
    error_invalid_input: "请检查填写内容和素材格式后重试。",
    error_invalid_reference: "参考素材无法读取。请使用 PNG、JPEG、WebP 图片或支持的视频。",
    error_reference_duration: "原视频与身份参考视频的时长总和不能超过 30 秒。",
    error_file_too_large: "文件过大。原视频上限为 500 MB，单份参考上限为 100 MB。",
    error_empty_file: "所选文件为空，请重新选择。",
    error_review_required: "请先检查并批准当前的引导视频。",
    error_review_changed: "引导素材发生变化，请刷新后重新检查。",
    error_job_busy: "任务正在处理中，请等待当前步骤完成。",
    error_already_submitted: "这个任务已有生成记录。请查看或继续获取原任务的结果。",
    error_mesh_unavailable: "人脸网格组件尚未安装。请运行项目的 setup-face-mesh.sh 后重试。",
    error_mesh_no_mask: "人脸网格模式无需重新分割。请检查追踪是否全程贴合。",
    error_no_saved_task: "没有可以继续获取的生成任务。",
    error_job_not_found: "找不到这个任务，请在左侧选择其他任务。",
    error_invalid_session: "页面会话已更新，请刷新页面后重试。",
    error_connection: "无法连接本地应用，请确认应用仍在运行。",
    error_prompt_too_long: "替换说明太长，请缩短后重试。",
    sourceLocked: "当前任务的原片已保存。更换原片请新建任务。",
    savedReference: "已保存的角色参考", paidRepairConfirm: "重新分割会再次调用 Replicate 并计费。继续吗？"
  },
  en: {
    newTask: "New task", recent: "Recent tasks", historyEmpty: "Your tasks stay here, ready to pick up later.",
    localWorkspace: "Local workspace", workspace: "Character replacement", settings: "API keys",
    title: "Character replacement studio", subtitle: "Prepare, inspect and generate with a workflow you can resume.",
    setupNotice: "Connect DreamAPI and Replicate to start your first task.", configure: "Connect",
    stepPrepare: "Prepare input", stepReview: "Review guidance", stepGenerate: "Generate & export",
    materials: "Input materials", sourceVideo: "Source video", required: "Required",
    chooseVideo: "Choose or drop a video", sourceHint: "4–30 sec · MP4 / MOV / WebM · With audio",
    advanced: "Preparation options", method: "Guidance method", modeDepth: "Depth + subject masks",
    modeMesh: "Face mesh · Centered speakers", modeBoth: "Depth + masks + face mesh", subject: "Subject to replace",
    subjectHint: "The default “person” selects detected people. Review masks carefully for multiple subjects.",
    prepare: "Prepare guidance", prepareCost: "This step uses paid Replicate processing.",
    character: "Target character", chooseReference: "Add a character reference", referenceHint: "Image or identity reference video",
    addSecond: "Add a second character (optional)", chooseImage: "Choose reference image", prompt: "Replacement instructions",
    promptHint: "Describe the replacement. Map references to people explicitly when using two characters.",
    resolution: "Output resolution", generate: "Generate finished video", generationGate: "Prepare and approve guidance to enable generation.",
    generationCost: "Generates the chosen resolution directly using paid DreamAPI processing.",
    preview: "Video preview", stateIdle: "Awaiting input", emptyTitle: "Start with a source video",
    emptyCopy: "Compare the original, motion guidance and finished video in this viewer.",
    originalAudio: "Original audio preserved in the finished video", download: "Download video",
    reviewTitle: "Review the entire clip before generating",
    reviewCopy: "Check hair, hands and clothing coverage, background spill, and face-mesh alignment throughout. Listen for speech and motion timing.",
    reviewConfirm: "I reviewed the entire guidance clip and am ready to generate.",
    approve: "Approve guidance", repair: "Re-segment from source",
    repairHint: "Re-segmentation uses paid Replicate processing. Review the full clip again afterward.",
    approved: "Guidance approved. Ready to generate.", attention: "This task needs attention", resume: "Resume result collection",
    resultReady: "Your video is ready", resultCopy: "Original audio restored. Check the character, motion and lip sync before downloading.",
    durationNote: "The generated tail was adjusted slightly to match the source duration. The original audio remains complete.",
    workflowNote: "Replicate prepares the guidance. DreamAPI generates the finished video at your selected resolution.",
    back: "Back to workspace", settingsTitle: "Connect your model services",
    settingsSubtitle: "Keys are saved in this Mac’s Keychain and loaded automatically next time.",
    dreamRole: "Seedance 2.5 generation and media uploads", replicateRole: "Vocal separation, depth and subject masks",
    saveKey: "Save key", getKey: "Get an API key", removeKey: "Remove saved key",
    keychainNote: "macOS may ask for Keychain access the first time. Allow this application’s Python to access it. The page only shows connection status; saved keys are never displayed.",
    keyBilling: "Saving a key connects your account. Processing is billed by each platform and requires available credit.",
    configured: "Configured", unconfigured: "Not connected", keySaved: "Key saved in macOS Keychain.", keyRemoved: "Saved key removed.",
    confirmRemove: "Remove the saved key for this service?", original: "Original", guidance: "Guidance",
    depth: "Depth", mask: "Mask", result: "Result", sourceLocal: "Source · Not uploaded yet", clipSeconds: "sec",
    jobCreated: "Preparing your source video.",
    state_preparing: "Preparing", state_repairing: "Re-segmenting", state_review: "Needs review", state_ready: "Ready",
    state_submitting: "Submitting", state_generating: "Generating", state_done: "Finished", state_error: "Needs attention",
    state_uncertain: "Check provider", state_interrupted: "Interrupted",
    stage_prepare: "Preparing source video", stage_audio: "Processing the original vocals",
    stage_depth: "Generating depth guidance", stage_mask: "Segmenting the subject", stage_composite: "Compositing guidance",
    stage_mesh: "Tracking facial motion", stage_upload: "Uploading generation inputs", stage_submitting: "Submitting the generation",
    stage_generate: "Seedance is generating your video", stage_restore: "Restoring original audio",
    stage_review: "Awaiting guidance review", stage_done: "Video ready",
    monitorIdle: "Ready for your source", monitorIdleCopy: "Every processing stage will appear here once you start.",
    monitorUploading: "Uploading source material", monitorUploadingCopy: "Creating the task and reading your clip. Progress will appear automatically.",
    monitorReview: "Guidance ready for your review", monitorReady: "Guidance approved. Ready to generate.",
    monitorError: "Processing paused · completed steps saved", monitorDone: "Your video is ready",
    step_input: "Upload", step_audio: "Vocals", step_depth: "Depth", step_mask: "Masks",
    step_mesh: "Face tracking", step_composite: "Guidance", step_review: "Approve", step_generate: "Generate", step_restore: "Audio restore",
    stepState_waiting: "Review needed", stepState_done: "Complete", stepState_active: "Processing", stepState_error: "Attention", stepState_pending: "Waiting",
    preparingAction: "Preparing…", generatingAction: "Generating…",
    retryPreparation: "Retry failed stage", retryChargeConfirm: "Retry only the confirmed failed stage. Completed results are reused. The model retry may incur a new charge. Continue?",
    resumePreparation: "Resume preparation",
    cloudQueued: "Replicate accepted the task and is queuing or starting the model. A successful request does not mean the video is ready.",
    cloudRunning: "Replicate is processing the video. Runtime depends on clip length and the model.",
    error_preparation_uncertain: "The preparation submission outcome is unclear. Check Replicate task history before deciding what to do next.",
    preparingCopy: "Preserving the source motion and timing. You can switch to other tasks while processing.",
    generatingCopy: "This usually takes a few minutes. Reopen this task to collect the same result if you close the page.",
    repairingCopy: "Repairing masks with details from the original footage. Review the full guidance again afterward.",
    selectSource: "Choose a source video first.", selectReference: "Add a target character reference.",
    error_provider_payment: "The cloud provider returned a payment or credit error (402). Check billing and available credit for the service used in this stage.",
    error_provider_auth: "The cloud provider rejected the key. Update that provider’s API key in Settings.",
    error_provider_error: "Cloud processing failed. Check the provider’s task history, media requirements and available credit.",
    error_network_error: "Could not reach the provider. Check your connection; existing generation tasks can resume result collection.",
    error_collection_timeout: "Result collection timed out. The task ID is saved; resume collection to check the same generation.",
    error_processing_error: "Processing did not complete. Check that the clip plays, the subject can be tracked, and the provider’s task history.",
    error_keys_required: "Connect the required provider in API keys first.",
    error_submission_uncertain: "The submission outcome is unclear. Check DreamAPI task history and billing before creating another task. Do not submit again until you confirm what happened.",
    error_preparation_interrupted: "Preparation was interrupted. Check Replicate’s task history before creating a new task and repeating paid preparation.",
    error_keychain_unavailable: "macOS Keychain is unavailable. Check system access permissions and try again.",
    error_invalid_key: "Enter a non-empty API key without spaces.",
    error_invalid_video: "Could not read the video. Choose a playable MP4, MOV or WebM file.",
    error_audio_required: "The source needs an audio track to preserve in the final export.",
    error_duration_range: "Source duration must be 4–30 seconds; reference videos must be 2–30 seconds.",
    error_invalid_input: "Check the entered values and media formats, then try again.",
    error_invalid_reference: "Could not read the reference. Use a PNG, JPEG, WebP image or a supported video.",
    error_reference_duration: "Source and identity reference videos must total no more than 30 seconds.",
    error_file_too_large: "File too large. Source limit is 500 MB; each reference limit is 100 MB.",
    error_empty_file: "This file is empty. Choose another file.",
    error_review_required: "Review and approve the current guidance before generating.",
    error_review_changed: "The prepared files changed. Reload and review them again.",
    error_job_busy: "This task is processing. Wait for the current step to finish.",
    error_already_submitted: "This task already has a generation record. View or resume the existing result.",
    error_mesh_unavailable: "Face mesh is not installed. Run setup-face-mesh.sh in the project first.",
    error_mesh_no_mask: "Face-mesh mode has no mask to repair. Check the tracking alignment instead.",
    error_no_saved_task: "There is no saved generation to resume.",
    error_job_not_found: "This task could not be found. Choose another task from the sidebar.",
    error_invalid_session: "The local session changed. Reload the page and try again.",
    error_connection: "Cannot reach the local application. Check that it is still running.",
    error_prompt_too_long: "Shorten the replacement instructions and try again.",
    sourceLocked: "The source for this task is saved. Create a new task to change it.",
    savedReference: "Saved character reference", paidRepairConfirm: "Re-segmentation calls Replicate again and incurs charges. Continue?"
  }
};

const $ = (selector) => document.querySelector(selector);
let language = localStorage.getItem("genjustsu.language") === "en" ? "en" : "zh";
let token = "";
let keys = {dreamapi: false, replicate: false};
let jobId = null;
let job = null;
let previousState = null;
let selectedPreview = "";
let sourceURL = "";
let referenceURL = "";
let pollTimer;
let toastTimer;
let historyItems = [];
let actionBusy = false;
let renderedPipelineKey = "";
const runningStates = ["preparing", "repairing", "submitting", "generating"];
const t = (key) => copy[language][key] || copy[language].error_processing_error;

function toast(message) {
  clearTimeout(toastTimer);
  $("#toast").textContent = message;
  $("#toast").hidden = false;
  toastTimer = setTimeout(() => { $("#toast").hidden = true; }, 6500);
}

async function api(url, options = {}) {
  let response;
  try {
    response = await fetch(url, {...options, headers: {...options.headers, "X-Local-Token": token}});
  } catch {
    throw new Error("connection");
  }
  let data;
  try { data = await response.json(); } catch { throw new Error("connection"); }
  if (!response.ok) throw new Error(typeof data.detail === "string" ? data.detail : "invalid_input");
  return data;
}

function errorMessage(error) {
  return t("error_" + (error.message || error));
}

function applyLanguage() {
  document.documentElement.lang = language === "zh" ? "zh-CN" : "en";
  document.querySelectorAll("[data-i18n]").forEach((element) => {
    element.textContent = t(element.dataset.i18n);
  });
  $("#language").textContent = language === "zh" ? "EN" : "中文";
  updatePromptCount();
  renderKeys();
  renderHistory();
  renderJob();
  if (!job) renderLocalSource();
}

function showSettings(visible) {
  $("#settings-view").hidden = !visible;
  $("#workspace").hidden = visible;
  if (visible) $("#dreamapi-key").focus();
}

function renderKeys() {
  $("#setup-notice").hidden = keys.dreamapi && keys.replicate;
  $("#key-dot").classList.toggle("ready", keys.dreamapi && keys.replicate);
  for (const provider of ["dreamapi", "replicate"]) {
    const status = $("#" + provider + "-status");
    status.textContent = t(keys[provider] ? "configured" : "unconfigured");
    status.classList.toggle("success", keys[provider]);
    document.querySelector('.remove-key[data-provider="' + provider + '"]').hidden = !keys[provider];
  }
}

async function refreshKeys() {
  keys = (await api("/api/keys")).providers;
  renderKeys();
  renderJob();
}

function renderHistory() {
  const history = $("#history");
  history.replaceChildren();
  $("#history-empty").hidden = historyItems.length > 0;
  $("#task-count").textContent = historyItems.length;
  for (const item of historyItems) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "history-item" + (item.id === jobId ? " active" : "");
    button.setAttribute("aria-current", item.id === jobId ? "true" : "false");
    const name = document.createElement("strong");
    name.textContent = item.name;
    name.title = item.name;
    const meta = document.createElement("small");
    meta.textContent = new Date(item.created_at).toLocaleDateString(language === "zh" ? "zh-CN" : "en-US", {month: "short", day: "numeric"}) + " · " + t("state_" + item.state);
    button.append(name, meta);
    button.onclick = () => selectJob(item.id);
    history.append(button);
  }
}

async function refreshHistory() {
  historyItems = await api("/api/jobs");
  renderHistory();
}

function mediaURL(filename) {
  const version = ["seedance-input.mp4", "mask.mp4"].includes(filename) ? job?.review?.fingerprint : "";
  return "/api/jobs/" + jobId + "/files/" + encodeURIComponent(filename) + (version ? "?v=" + encodeURIComponent(version) : "");
}

function setPreview(filename) {
  selectedPreview = filename;
  const video = $("#preview-video");
  const oldTime = Number.isFinite(video.currentTime) ? video.currentTime : 0;
  const url = mediaURL(filename);
  if (video.getAttribute("src") !== url) {
    video.onloadedmetadata = () => {
      if (Number.isFinite(video.duration)) video.currentTime = Math.min(oldTime, Math.max(0, video.duration - 0.05));
    };
    video.src = url;
    video.load();
  }
  video.hidden = false;
  $("#empty-preview").hidden = true;
  $("#media-stage").classList.add("has-video");
  $("#download").hidden = false;
  $("#download").href = url;
  $("#download").download = filename === "final-preview.mp4" ? "genjustsu-" + jobId.slice(0, 8) + ".mp4" : filename;
  const label = {"upload.mp4": "original", "original.mp4": "original", "seedance-input.mp4": "guidance", "depth.mp4": "depth", "mask.mp4": "mask", "final-preview.mp4": "result"};
  $("#preview-caption").textContent = t(label[filename]) + (filename === "final-preview.mp4" ? " · " + t("originalAudio") : "");
  document.querySelectorAll("#preview-tabs button").forEach((button) => {
    button.classList.toggle("active", button.dataset.file === filename);
    button.setAttribute("aria-pressed", String(button.dataset.file === filename));
  });
}

function renderLocalSource() {
  if (job) return;
  const file = $("#source-file").files[0];
  $("#source-name").textContent = file ? file.name : t("chooseVideo");
  if (!file || !sourceURL) return;
  $("#preview-video").src = sourceURL;
  $("#preview-video").hidden = false;
  $("#empty-preview").hidden = true;
  $("#media-stage").classList.add("has-video");
  $("#preview-caption").textContent = t("sourceLocal");
}

function renderJob() {
  renderExecution();
  const selectedReference = $("#reference-file").files[0];
  const savedReference = job?.references?.some(name => name.startsWith("reference-1"));
  $("#reference-name").textContent = selectedReference?.name || t(savedReference ? "savedReference" : "chooseReference");
  $("#workspace").classList.toggle("has-guidance", Boolean(job?.files.includes("seedance-input.mp4")));
  const busy = Boolean(job && runningStates.includes(job.state));
  $("#prepare-button span").textContent = t(busy && ["preparing", "repairing"].includes(job.state) ? "preparingAction" : "prepare");
  $("#generate-button span").textContent = t(busy && ["submitting", "generating"].includes(job.state) ? "generatingAction" : "generate");
  $("#prepare-button").setAttribute("aria-busy", String(actionBusy || busy));
  $("#generate-button").setAttribute("aria-busy", String(actionBusy || busy));
  $("#prepare-button").disabled = actionBusy || busy || Boolean(job) || !keys.replicate;
  $("#source-file").disabled = Boolean(job);
  $("#mode").disabled = Boolean(job);
  $("#subject").disabled = Boolean(job);
  $("#generate-button").disabled = actionBusy || !job || !keys.dreamapi || !job.review?.approved ||
    !["ready", "error"].includes(job.state) || Boolean(job.task_submitted);
  $("#reference-file").disabled = busy || Boolean(job?.task_submitted);
  $("#second-reference").disabled = busy || Boolean(job?.task_submitted);
  $("#prompt").disabled = busy || Boolean(job?.task_submitted);
  $("#resolution").disabled = busy || Boolean(job?.task_submitted);
  $("#generate-help").textContent = t(job?.review?.approved ? "generationCost" : "generationGate");
  $("#state-label").textContent = t(job ? "state_" + job.state : "stateIdle");
  $("#state-label").classList.toggle("success", ["ready", "done"].includes(job?.state));
  $("#task-progress").hidden = !busy;
  $("#review-panel").hidden = !job || job.state !== "review";
  $("#approved-note").hidden = !job || job.state !== "ready";
  $("#result-note").hidden = !job || job.state !== "done";
  $("#job-error").hidden = !job?.error;
  if (job?.error) {
    const provider = ["prepare", "audio", "depth", "mask", "composite", "mesh"].includes(job.stage) ? "Replicate" : "DreamAPI";
    const providerError = ["provider_payment", "provider_auth", "provider_error"].includes(job.error);
    $("#job-error-message").textContent = (providerError ? provider + " · " : "") + t("error_" + job.error);
  }
  $("#resume-button").hidden = !job?.can_resume;
  $("#resume-prepare-button").hidden = !job?.can_resume_preparation;
  $("#resume-prepare-button").textContent = t(job?.retry_preparation_stage ? "retryPreparation" : "resumePreparation");
  $("#repair-button").hidden = job?.mode === "face_mesh";
  $("#repair-hint").hidden = job?.mode === "face_mesh";
  $("#duration-note").hidden = !job?.duration_adjusted;
  if (!job) {
    $("#source-duration").textContent = "";
      return;
  }
  $("#source-name").textContent = job.name;
  $("#source-name").title = t("sourceLocked");
  $("#source-duration").textContent = job.duration.toFixed(1) + " " + t("clipSeconds");
  $("#mode").value = job.mode;
  $("#subject").value = job.subject;
  $("#progress-title").textContent = t("stage_" + job.stage);
  $("#progress-copy").textContent = t(job.state === "repairing" ? "repairingCopy" :
    ["submitting", "generating"].includes(job.state) ? "generatingCopy" : "preparingCopy");
  if (["preparing", "repairing"].includes(job.state)) {
    if (job.provider_status === "starting") $("#progress-copy").textContent = t("cloudQueued");
    if (job.provider_status === "processing") $("#progress-copy").textContent = t("cloudRunning");
  }
  const elapsed = Math.max(0, Math.floor((Date.now() - Date.parse(job.created_at)) / 1000));
  $("#progress-time").textContent = Math.floor(elapsed / 60) + ":" + String(elapsed % 60).padStart(2, "0");
  const files = [
    ["upload.mp4", "original"], ["seedance-input.mp4", "guidance"],
    ["depth.mp4", "depth"], ["mask.mp4", "mask"], ["final-preview.mp4", "result"]
  ].filter(([filename]) => job.files.includes(filename));
  $("#preview-tabs").replaceChildren();
  for (const [filename, label] of files) {
    const button = document.createElement("button");
    button.type = "button";
    button.dataset.file = filename;
    button.textContent = t(label);
    button.onclick = () => setPreview(filename);
    $("#preview-tabs").append(button);
  }
  if (previousState !== job.state) {
    $("#review-check").checked = false;
    $("#approve-button").disabled = true;
    if (job.state === "done") selectedPreview = "final-preview.mp4";
    if (job.state === "review") selectedPreview = "seedance-input.mp4";
  }
  previousState = job.state;
  if (files.length) {
    if (!files.some(([filename]) => filename === selectedPreview)) selectedPreview = files[0][0];
    setPreview(selectedPreview);
  }
}

function renderExecution() {
  const busy = Boolean(job && runningStates.includes(job.state));
  const failed = Boolean(job?.error);
  $("#execution-panel").classList.toggle("is-running", busy || actionBusy);
  $("#execution-panel").classList.toggle("has-error", failed);
  $("#execution-indicator").classList.toggle("spinning", busy || actionBusy);
  let title = t("monitorIdle");
  let description = t("monitorIdleCopy");
  if (actionBusy && !job) {
    title = t("monitorUploading");
    description = t("monitorUploadingCopy");
  } else if (job) {
    title = failed ? t("monitorError") : job.state === "done" ? t("monitorDone") :
      job.state === "review" ? t("monitorReview") : job.state === "ready" ? t("monitorReady") : t("stage_" + job.stage);
    description = job.name;
    if (job.provider_status === "starting") description = t("cloudQueued");
    if (job.provider_status === "processing") description = t("cloudRunning");
  }
  $("#execution-title").textContent = title;
  $("#execution-description").textContent = description;
  const fallback = ["input", "audio", "depth", "mask", "composite", "review", "generate", "restore"].map(id => ({id, state: "pending"}));
  const stages = job?.pipeline || fallback;
  $("#execution-count").textContent = stages.filter(stage => stage.state === "done").length + " / " + stages.length;
  const pipelineKey = JSON.stringify([jobId, language, stages]);
  if (pipelineKey !== renderedPipelineKey) {
  renderedPipelineKey = pipelineKey;
  const strip = $("#pipeline");
  const previousScroll = strip.scrollLeft;
  strip.replaceChildren();
  for (const stage of stages) {
    const item = document.createElement("div");
    item.className = "pipeline-stage " + stage.state;
    item.setAttribute("role", "listitem");
    const indicator = document.createElement("span");
    indicator.className = "stage-indicator";
    indicator.setAttribute("aria-hidden", "true");
    const text = document.createElement("span");
    text.className = "stage-text";
    const label = document.createElement("strong");
    label.textContent = t("step_" + stage.id);
    const state = document.createElement("small");
    state.textContent = t("stepState_" + stage.state);
    text.append(label, state);
    item.append(indicator, text);
    strip.append(item);
  }
  strip.scrollLeft = previousScroll;
  const current = strip.querySelector(".error, .active, .waiting");
  if (current && strip.scrollWidth > strip.clientWidth) {
    const relativeLeft = current.getBoundingClientRect().left - strip.getBoundingClientRect().left;
    strip.scrollLeft += relativeLeft - (strip.clientWidth - current.offsetWidth) / 2;
  }
  }
  renderElapsed();
}

function renderElapsed() {
  let seconds = 0;
  if (job) {
    const end = runningStates.includes(job.state) ? Date.now() : Date.parse(job.updated_at || job.created_at);
    seconds = Math.max(0, Math.floor((end - Date.parse(job.created_at)) / 1000));
  }
  $("#execution-elapsed").textContent = String(Math.floor(seconds / 60)).padStart(2, "0") + ":" + String(seconds % 60).padStart(2, "0");
}
setInterval(renderElapsed, 1000);

async function pollJob(ident) {
  clearTimeout(pollTimer);
  try {
    const result = await api("/api/jobs/" + ident);
    if (ident !== jobId) return;
    const changed = job?.state !== result.state;
    job = result;
    renderJob();
    if (changed) await refreshHistory();
    if (runningStates.includes(job.state)) pollTimer = setTimeout(() => pollJob(ident), 2500);
  } catch (error) {
    if (ident !== jobId) return;
    toast(errorMessage(error));
    pollTimer = setTimeout(() => pollJob(ident), 8000);
  }
}

function clearFiles() {
  if (sourceURL) URL.revokeObjectURL(sourceURL);
  if (referenceURL) URL.revokeObjectURL(referenceURL);
  sourceURL = referenceURL = "";
  $("#source-file").value = "";
  $("#reference-file").value = "";
  $("#second-reference").value = "";
  $("#reference-image").hidden = true;
  $("#reference-icon").toggleAttribute("hidden", false);
  $("#reference-name").textContent = t("chooseReference");
  $("#second-name").textContent = "";
  $("#preview-video").pause();
  $("#preview-video").onloadedmetadata = null;
  $("#preview-video").removeAttribute("src");
  $("#preview-video").load();
  $("#preview-video").hidden = true;
  $("#empty-preview").hidden = false;
  $("#media-stage").classList.remove("has-video");
  $("#download").hidden = true;
  $("#preview-tabs").replaceChildren();
}

async function selectJob(ident) {
  clearTimeout(pollTimer);
  clearFiles();
  jobId = ident;
  job = null;
  previousState = null;
  selectedPreview = "";
  localStorage.setItem("genjustsu.lastTask", ident);
  showSettings(false);
  await pollJob(ident);
  if (job?.prompt) {
    $("#prompt").value = job.prompt;
    $("#prompt").dataset.edited = "true";
  } else $("#prompt").value = WORKFLOW_DEFAULT_PROMPT;
  if (job?.resolution) $("#resolution").value = job.resolution;
  const reference = job?.references.find((name) => name.startsWith("reference-1"));
  if (reference) {
    $("#reference-name").textContent = t("savedReference");
    if (/\.(png|jpe?g|webp)$/i.test(reference)) {
      $("#reference-image").src = mediaURL(reference);
      $("#reference-image").hidden = false;
      $("#reference-icon").toggleAttribute("hidden", true);
    }
  }
  updatePromptCount();
  renderHistory();
}

function newTask() {
  clearTimeout(pollTimer);
  jobId = job = previousState = null;
  selectedPreview = "";
  clearFiles();
  localStorage.removeItem("genjustsu.lastTask");
  $("#source-name").textContent = t("chooseVideo");
  $("#prompt").value = WORKFLOW_DEFAULT_PROMPT;
  delete $("#prompt").dataset.edited;
  $("#mode").value = "depth";
  $("#subject").value = "person";
  $("#preview-caption").textContent = t("originalAudio");
  $("#resolution").value = "720p";
  showSettings(false);
  renderJob();
  renderHistory();
  updatePromptCount();
}

function updatePromptCount() {
  $("#prompt-count").textContent = $("#prompt").value.length + " / 950";
}

$("#language").onclick = () => {
  language = language === "zh" ? "en" : "zh";
  localStorage.setItem("genjustsu.language", language);
  applyLanguage();
};
$("#new-task").onclick = newTask;
$("#settings-open").onclick = $("#setup-open").onclick = () => showSettings(true);
$("#settings-back").onclick = () => showSettings(false);
$("#prompt").oninput = () => { $("#prompt").dataset.edited = "true"; updatePromptCount(); };

$("#source-file").onchange = () => {
  if (sourceURL) URL.revokeObjectURL(sourceURL);
  sourceURL = $("#source-file").files[0] ? URL.createObjectURL($("#source-file").files[0]) : "";
  renderLocalSource();
};
for (const event of ["dragenter", "dragover"]) $("#source-drop").addEventListener(event, (e) => {
  e.preventDefault();
  if (!job) $("#source-drop").classList.add("dragover");
});
$("#source-drop").addEventListener("dragleave", () => $("#source-drop").classList.remove("dragover"));
$("#source-drop").addEventListener("drop", (e) => {
  e.preventDefault();
  $("#source-drop").classList.remove("dragover");
  if (job || !e.dataTransfer.files.length) return;
  const transfer = new DataTransfer();
  transfer.items.add(e.dataTransfer.files[0]);
  $("#source-file").files = transfer.files;
  $("#source-file").dispatchEvent(new Event("change"));
});
$("#reference-file").onchange = () => {
  const file = $("#reference-file").files[0];
  if (!file) return;
  $("#reference-name").textContent = file.name;
  if (referenceURL) URL.revokeObjectURL(referenceURL);
  const image = /\.(png|jpe?g|webp)$/i.test(file.name);
  $("#reference-image").hidden = !image;
  $("#reference-icon").toggleAttribute("hidden", image);
  if (image) {
    referenceURL = URL.createObjectURL(file);
    $("#reference-image").src = referenceURL;
  }
};
$("#second-reference").onchange = () => {
  $("#second-name").textContent = $("#second-reference").files[0]?.name || "";
};

$("#source-form").onsubmit = async (event) => {
  event.preventDefault();
  if (job || actionBusy) return;
  if (!$("#source-file").files.length) return toast(t("selectSource"));
  actionBusy = true;
  renderJob();
  try {
    const data = new FormData(event.target);
    const response = await api("/api/jobs", {method: "POST", body: data});
    // Keep the character selection made before preparation.
    jobId = response.id;
    localStorage.setItem("genjustsu.lastTask", jobId);
    previousState = null;
    selectedPreview = "";
    await refreshHistory();
    await pollJob(jobId);
    toast(t("jobCreated"));
  } catch (error) {
    toast(errorMessage(error));
  } finally {
    actionBusy = false;
    renderJob();
  }
};

$("#review-check").onchange = () => { $("#approve-button").disabled = !$("#review-check").checked; };
$("#approve-button").onclick = async () => {
  if (!job || !$("#review-check").checked) return;
  $("#approve-button").disabled = true;
  try {
    await api("/api/jobs/" + jobId + "/review", {
      method: "POST", headers: {"Content-Type": "application/json"},
      body: JSON.stringify({approved: true, fingerprint: job.review.fingerprint})
    });
    await pollJob(jobId);
  } catch (error) {
    toast(errorMessage(error));
    $("#approve-button").disabled = !$("#review-check").checked;
  }
};
$("#repair-button").onclick = async () => {
  if (!job || !confirm(t("paidRepairConfirm"))) return;
  $("#repair-button").disabled = true;
  try {
    await api("/api/jobs/" + jobId + "/repair", {method: "POST"});
    await pollJob(jobId);
  } catch (error) { toast(errorMessage(error)); }
  finally { $("#repair-button").disabled = false; }
};

async function referenceFile(input, number) {
  if (input.files[0]) return input.files[0];
  const saved = job?.references.find((name) => name.startsWith("reference-" + number));
  if (!saved) return null;
  const response = await fetch(mediaURL(saved));
  if (!response.ok) throw new Error("invalid_reference");
  return new File([await response.blob()], saved);
}

$("#generate-form").onsubmit = async (event) => {
  event.preventDefault();
  if (!job || actionBusy) return;
  actionBusy = true;
  renderJob();
  try {
    const reference = await referenceFile($("#reference-file"), 1);
    if (!reference) throw new Error("select_reference");
    const data = new FormData(event.target);
    data.set("reference", reference);
    const second = await referenceFile($("#second-reference"), 2);
    if (second) data.set("second_reference", second);
    else data.delete("second_reference");
    await api("/api/jobs/" + jobId + "/generate", {method: "POST", body: data});
    await pollJob(jobId);
  } catch (error) {
    toast(error.message === "select_reference" ? t("selectReference") : errorMessage(error));
  } finally {
    actionBusy = false;
    renderJob();
  }
};
$("#resume-prepare-button").onclick = async () => {
  if (job?.retry_preparation_stage && !confirm(t("retryChargeConfirm"))) return;
  $("#resume-prepare-button").disabled = true;
  try {
    await api("/api/jobs/" + jobId + (job?.retry_preparation_stage ? "/retry-preparation" : "/resume-preparation"), {method: "POST"});
    await pollJob(jobId);
  } catch (error) { toast(errorMessage(error)); }
  finally { $("#resume-prepare-button").disabled = false; }
};

$("#resume-button").onclick = async () => {
  $("#resume-button").disabled = true;
  try {
    await api("/api/jobs/" + jobId + "/resume", {method: "POST"});
    await pollJob(jobId);
  } catch (error) { toast(errorMessage(error)); }
  finally { $("#resume-button").disabled = false; }
};

for (const form of document.querySelectorAll(".key-form")) {
  form.onsubmit = async (event) => {
    event.preventDefault();
    const input = form.querySelector("input");
    const button = form.querySelector("button");
    button.disabled = true;
    try {
      await api("/api/keys/" + form.dataset.provider, {
        method: "PUT", headers: {"Content-Type": "application/json"}, body: JSON.stringify({value: input.value})
      });
      input.value = "";
      await refreshKeys();
      toast(t("keySaved"));
    } catch (error) { toast(errorMessage(error)); }
    finally { button.disabled = false; }
  };
}
for (const button of document.querySelectorAll(".remove-key")) {
  button.onclick = async () => {
    if (!confirm(t("confirmRemove"))) return;
    button.disabled = true;
    try {
      await api("/api/keys/" + button.dataset.provider, {method: "DELETE"});
      await refreshKeys();
      toast(t("keyRemoved"));
    } catch (error) { toast(errorMessage(error)); }
    finally { button.disabled = false; }
  };
}

async function boot() {
  $("#prompt").value = WORKFLOW_DEFAULT_PROMPT;
  applyLanguage();
  try {
    token = (await api("/api/session")).token;
    await refreshKeys();
    await refreshHistory();
    const saved = localStorage.getItem("genjustsu.lastTask");
    if (saved && historyItems.some((item) => item.id === saved)) await selectJob(saved);
  } catch (error) { toast(errorMessage(error)); }
}
boot();
