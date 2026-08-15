# TP导演 Production Engine V2.4

仅使用 Python 标准库；转写后端和 FFmpeg 为可选外部依赖。

```bash
python tp.py validate plan.json
python tp.py review plan.json --output review.md
python tp.py approve plan.json --shots B001,B003 --confirmation CONFIRM_H3_COST
python tp.py dry-run plan.json
python tp.py generate plan.json --approved
python tp.py roughcut plan.json --source talking-head.mp4 --generated-dir generated --output roughcut.mp4
python tp.py probe clip.mp4
python tp.py route-template "解释两个系统的差异"
```

真实生成前：先 review → 用户明确批准 → approve → dry-run → generate --approved。
