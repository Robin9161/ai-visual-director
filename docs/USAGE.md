# TP导演 V2.4 使用流程

## 一次完整项目
1. 输入 SRT/逐字稿/口播视频。
2. Research → Blocker。
3. Art Direction → 用户确认 → World/Master Lock。
4. Visual Beat/Shot + T01–T21 可选路由。
5. Asset Audit + Plan Validator。
6. Production Keyframe Gate。
7. H3 Prompt + avd-plan.json。
8. `avd.py review`。
9. 用户明确批准 → `avd.py approve ... --confirmation CONFIRM_H3_COST`。
10. `avd.py dry-run`。
11. `MINIMAX_API_KEY=... avd.py generate ... --approved`。
12. ffprobe + Visual Critic。
13. `avd.py roughcut`。
14. Whole-film QA。
15. Precision/Final。

## 哪些是 V2.4 真代码
Validator、Approval Gate、Asset Blocking、Dry-run、H3 请求/轮询/下载/Manifest、Template Router、ffprobe、Whisper 入口、FFmpeg rough cut。

## 哪些仍由 Agent/人工完成
事实研究、Art Direction、World/MASTER 图片生成、真正视觉审片、Production Keyframe 美学判断、Whole-film 审美判断、复杂剪辑软件原生时间线。
