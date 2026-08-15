---
name: visual-critic
description: 对 Preview/Production Keyframe、生成视频、粗剪和 Final 做严格 QA；必须记录实际视觉输入 VIDEO_DIRECT/MULTI_FRAME/CONTACT_SHEET/KEYFRAME_ONLY，没有看到素材不得伪造精确分数。
---
# Visual Critic V2.4

## 结论
PASS / RETRY / RETURN / REJECT。

## Keyframe QA
Visual Purpose、Composition、World、MASTER、Factual Fidelity、Cleanliness、Precision Ready。

## Shot QA
动作、稳定、闪烁、穿帮、人物/资产漂移、Precision 可用性、Audio Contract。

## Whole-film QA
必须基于真实 Rough Cut；检查 Motif、Grammar、Complexity、AI Fatigue、Talking-head Rhythm、信息密度、Shot Duration、World/Precision Continuity。

## Visual Input Verification
VIDEO_DIRECT / MULTI_FRAME / CONTACT_SHEET / KEYFRAME_ONLY / NOT_VISUALLY_VERIFIED。NOT_VISUALLY_VERIFIED 不得精确打分。

## Routing
FACT→Research；STYLE/MASTER→Art；DIRECTORIAL/RENDER_MEDIUM/MOTIF/CLEANLINESS_DESIGN→Visual；PROMPT/CLEAN_PLATE_EXECUTION→H3 Prompt；随机生成缺陷→RETRY；技术媒体错误→Engine。
