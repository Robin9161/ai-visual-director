# Changelog

## V2.4.0

- 产品主体正式命名为 **TP导演（TP Director）**；仓库 slug 与 AVD schema ID 暂保留以兼容既有安装和数据。

在 V2.3.1 全部创作规则基础上，新增可执行 Production Engine：

- AVD Plan Schema 2.4：统一 source/research/world/assets/beats/shots/approval/audio/edit/manifest 数据。
- 机械 Validator：把核心规则从“提示词要求”变成“程序不通过就不继续”。
- Approval Gate：未明确批准的 Shot 不能真实付费生成。
- Dry-run：正式 H3 请求前打印真实 payload，不联网、不花钱。
- Asset Request / Blocking：缺真实证据、Logo、UI、历史资料、技术拓扑时阻断相关 Shot。
- H3 API Adapter：提交、轮询、下载、Generation Manifest。
- Whisper Transcription：口播视频 → 带时间戳逐字稿。
- FFmpeg Rough Cut：按时间码 Fullscreen Replace，保留原口播音轨。
- Audio SFX Policy：禁止 AI 音乐/对白/旁白，仅允许命名拟音与克制环境声。
- T01–T21：作为 Visual Director 的 Packaging Pattern Library。
- Template Router：根据视觉目的提供模板候选，但不自动覆盖导演决定。
- World Board / MASTER Asset / Production Keyframe 三层资产层级继续保留。
- SCRIPT_BLOCKER、Visual Cleanliness、Precision、Historical Reconstruction、Whole-film QA 全部继续保留。

## V2.3.1

- 正式区分 World Board、MASTER Asset Pack 与 Production Keyframe。
- MASTER 单独资产图、版本管理、Cleanliness 规则。

## V2.3

- SCRIPT_BLOCKER、Render Medium、Handle Rule、Precision Manifest、Visual Cleanliness、Preview/Production Keyframe、Historical Reconstruction、真实看片 QA、粗剪后 Whole-film QA。
