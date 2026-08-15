#!/usr/bin/env python3
import json
from pathlib import Path

def load_templates():
    p=Path(__file__).resolve().parent.parent/'configs'/'template_library.json';return json.loads(p.read_text(encoding='utf-8'))

def recommend(text:str):
    t=text.lower();rules=[
      (['数字','比例','排名','倍','亿','万'],'T03'),(['论文','报告','引用','证据','文章'],'T04'),(['流程','因果','依赖','经过'],'T05'),(['章节','步骤','阶段'],'T07'),(['对比','相比','两边','开放','封闭','分裂'],'T14'),(['人物','创始','贡献','生平','程序员'],'T16'),(['组装','零件','模块','部件'],'T17'),(['地图','全球','地区','地点','路线'],'T18'),(['演进','时间线','历史','代际','年代'],'T19'),(['分类','分支','能力树','技术栈'],'T20'),(['原理','机制','编码','协议','信号','传感器','内部'],'T21')]
    ids=[]
    for keys,tid in rules:
        if any(k in t for k in keys):ids.append(tid)
    if not ids:ids=['T01','T02','T09']
    lib={x['id']:x for x in load_templates()};return [lib[x] for x in ids[:4]]
