# TP导演（TP Director）V2.4

TP导演是一套面向口播、知识类与科技内容的 AI 视觉导演与制片流水线。V2.4 把 V2.3.1 的“导演/美术/研究/质检大脑”与一个真正可运行的轻量 Production Engine 合并。

> 产品主体名称：**TP导演**（TP Director）。仓库 slug 暂保留 `ai-visual-director`，以兼容既有安装路径与脚本引用。

## 五个创作 Skill

1. `research-director`：事实研究、来源、SCRIPT_BLOCKER、历史重建边界。
2. `art-director`：3–5 个美术方向、World Board、World Bible、MASTER Asset Pack、Visual Motif。
3. `visual-director`：Visual Beat、ABC、Shot Role、Render Medium、Grammar、Complexity、Silent Test、Handle、Candidate Budget、模板路由。
4. `h3-prompt-director`：把批准 Shot 编译成 H3 可执行 Prompt，遵守 capability、Precision、Clean Plate 与 Audio SFX Policy。
5. `visual-critic`：Production Keyframe、视频、粗剪、Final QA；必须真正看到视觉输入。

## V2.4 新增的可执行 Production Engine

`production-engine/` 已包含可运行脚本：

- `avd.py`：统一 CLI。
- `plan_tool.py`：机械 Validator、Review、Approval Gate、Blocker Gate。
- `h3_adapter.py`：MiniMax H3 API Adapter + Dry-run + Generation Manifest。
- `transcribe_video.py`：Whisper/Faster-Whisper/MLX-Whisper 自动转写入口。
- `roughcut.py`：FFmpeg 时间戳粗剪；保留原口播音轨，只低音量混合 SFX。
- `media_probe.py`：ffprobe 技术 QA。
- `template_router.py`：T01–T21 作为工具箱推荐，不取代 Visual Director。

## V2.4 核心融合原则

- `World Board ≠ MASTER Asset ≠ Production Keyframe`。
- `Skill 负责判断，Engine 负责机械执行`。
- `T01–T21 是 Visual Director 的模板工具箱，不是导演本身`。
- `AI Coverage ≠ AI Final Usage`。
- `真实证据/Logo/UI/历史人物/技术关系` 缺资产时可 BLOCK。
- 付费 H3 请求必须同时通过 Approval Gate + Asset Gate，并显式 `--approved`。
- 正式请求前先 `--dry-run`。
- 重要文字、数字、Logo、代码、真实 UI 优先 Precision Layer / Hyperframes / Real Evidence，而不是赌 H3。
- Rough Cut 后才做 Whole-film QA。

## 目录

```text
research-director/
art-director/
visual-director/
h3-prompt-director/
visual-critic/
production-engine/
schemas/
configs/
template-library/
docs/
examples/
tests/
```

## 快速开始

```bash
cd production-engine
python tp.py validate ../examples/ffmpeg-90s-plan.example.json
python tp.py review ../examples/ffmpeg-90s-plan.example.json
python tp.py dry-run ../examples/ffmpeg-90s-plan.example.json
```

真实 H3 生成需要 `MINIMAX_API_KEY`，且必须先批准具体 Shot。

## 第三方来源

V2.4 的 Production Engine 设计吸收了 Guangjun 的 `minimax-h3-broll-generator` 1.1.0 的若干 MIT 开源思想与接口模式，包括 approval/dry-run、asset blocking、H3 adapter、Whisper 输入、generation manifest、FFmpeg rough cut、audio SFX policy 与 T01–T21 模板库。详见 `THIRD_PARTY_NOTICES.md`。
