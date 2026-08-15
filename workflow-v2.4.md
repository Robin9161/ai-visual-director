# V2.4 全流程

1. 导入 SRT / 逐字稿 / Talking-head 视频。
2. Engine 做 SRT/Whisper 转写与轻量 ASR 清洗；原始输入不可覆盖。
3. Research Director 查真实人物、产品、数据、历史、地点、软件；生成 Research Pack。
4. 关键事实冲突 → `SCRIPT_BLOCKER`；Engine 阻断正式 Shot/H3。
5. Art Director 提 3–5 个真正不同的 Art Direction；每方向做 Preview Keyframe。
6. 用户选方向 → `STYLE_LOCK`。
7. 生成 World Board / World Bible / MASTER Asset Packs；锁定版本。
8. Visual Director 按 Visual Beat 拆稿；先选 Render Medium，再设计 Shot。
9. 对适合 Packaging Pattern 的镜头，查询 T01–T21；模板只是候选，Visual Director 可选 `NONE`。
10. Engine 运行 Asset Audit；真实证据/Logo/UI/历史人物/技术关系缺失时生成 `ASSET_BLOCKER`。
11. Shot Spec 必须含 Grade、Role、Render Medium、Grammar、Complexity、Silent Test、Motif、Handle、Precision、Keyframe Mode、Candidate Count。
12. Engine Validator 机械检查 Schema、Candidate Budget、Blocker、Approval、时长、Precision、Audio Policy。
13. Production Keyframe Gate：Cleanliness、World、MASTER、Composition、Precision Ready、Factual Fidelity。
14. H3 Prompt Director 编译 Prompt；读取真实 H3 capability，非 H3 Render Medium 不强制生成。
15. 生成 `avd-plan.json` + `review.md`。
16. 用户明确批准具体 Shot；Engine 写 Approval 状态。
17. `dry-run` 输出实际 H3 payload，不联网。
18. 再次确认后用 `--approved` 执行 H3；写 `generation-manifest.json`。
19. Engine 先做 ffprobe 技术 QA；Critic 真正看 VIDEO_DIRECT 或 MULTI_FRAME/CONTACT_SHEET。
20. 同一设计+Prompt 连续两轮失败 → RETURN，不无限抽卡。
21. 通过的候选按时间码生成低清 Rough Cut；原口播音轨持续保留，生成音频只允许 SFX/环境声。
22. Visual Critic 基于 Rough Cut 做 Whole-film QA：Motif、Grammar、Complexity、AI Fatigue、Talking-head Rhythm、信息密度、连续性。
23. Whole-film QA 后，仅对最终采用镜头投入 Precision Layer / 超分 / 精细合成。
24. Final QA → Editing Package。
