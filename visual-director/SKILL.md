---
name: visual-director
description: 把完整口播按 Visual Beat 拆成可生产 Shot；决定 ABC、HERO/PRIMARY/SUPPORT、Render Medium、Visual Grammar、Complexity、Silent Test、Motif State、Handle、Precision、Candidate Budget、Keyframe Mode，并可查询 T01–T21 作为模板工具箱。不要写最终 H3 Prompt。
---
# Visual Director V2.4

## 先决定 Render Medium
H3_VIDEO / KEYFRAME_MOTION / MOTION_GRAPHICS / REAL_REFERENCE / HYBRID / TALKING_HEAD。

## Beat 与 Shot
一个 Visual Beat = 一个完整视觉意思，不等于 SRT 一行。Beat 可拆 Shot，Role=HERO/PRIMARY/SUPPORT。

## ABC / Candidate Budget
A HERO=3，其他通常1；A 无 HERO 时主 PRIMARY=3。B 主 PRIMARY=2，其他1。C=1。技术难度只给主 Shot +1，通常 cap 3。

## Silent Test
A≥80%，B≥65%。

## Grammar / Complexity
连续3 Beat至少2种 Grammar；连续2 Shot不得同时重复景别+运镜+Grammar。
Complexity=LOW/MEDIUM/HIGH/HERO，避免连续视觉轰炸。

## Handle
默认建议 in 0.3–0.5s，out 0.3–0.8s；受模型真实时长档约束。

## Precision
NONE / POST_OVERLAY / SCREEN_REPLACE / SURFACE_TRACK。

## Keyframe
PREVIEW / PRODUCTION / SKIP。Production 必须过 Cleanliness、World、MASTER、Composition、Precision Ready。

## T01–T21
先决定信息载体和视觉目的，再查模板。模板可以返回 NONE；不得为了模板把真实证据变成 H3 伪证据，也不得破坏 World Bible / Motif。

使用 `references/shot-spec-template.md`、`render-medium.md`、`template-routing.md`、`candidate-budget.md`、`precision-layer.md`。
