# Codex 安装 TP导演 V2.4

把五个 Skill 目录放到项目 `.agents/skills/`：research-director / art-director / visual-director / h3-prompt-director / visual-critic。
把其余 `production-engine/ configs/ schemas/ template-library/ workflow-v2.4.md integration-contract.md` 保留在项目根的 `ai-visual-director/`。

建议第一次显式顺序调用五个 Skill；Production Engine 通过终端执行 `python production-engine/avd.py ...`。
