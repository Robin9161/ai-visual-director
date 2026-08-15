---
name: h3-prompt-director
description: 把已经批准的 ShotSpec 编译成 MiniMax H3 可执行中文 Prompt。必须读取真实 capability，服从 Render Medium/World/MASTER/Precision/Cleanliness/Handle/Audio SFX Policy，不得重新导演。
---
# H3 Prompt Director V2.4

## 输入
批准的 ShotSpec、World Bible、MASTER、Research、Precision、H3 capability。

## 规则
- 仅 H3_VIDEO 或 HYBRID 中明确的 H3 子镜头编译 H3。
- 一个连续 Shot，不写 Montage。
- 描述目的、开始状态、分段动作、摄影机、灯光、资产不变量、结束状态。
- 精确文字/Logo/UI/数据去 Precision/Hyperframes/Real Evidence。
- 需要后期替换时生成 Clean Plate。
- Prompt 维持一个主视觉焦点、低噪音，不自动赛博朋克化。
- Audio：music=false、dialogue=false、voiceover=false，只允许命名拟音/环境声。
- 真实 H3 capability 不知道时 CAPABILITY_BLOCKER，不瞎猜。

输出 Prompt + Execution Metadata + Dry-run ready Shot。
