#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,sys
from pathlib import Path
from plan_tool import load_plan,validate_plan,review_markdown,approve,CONFIRMATION
import h3_adapter, roughcut, template_router
from media_probe import probe

def main():
    p=argparse.ArgumentParser(prog='tp-director');sp=p.add_subparsers(dest='cmd',required=True)
    x=sp.add_parser('validate');x.add_argument('plan',type=Path)
    x=sp.add_parser('review');x.add_argument('plan',type=Path);x.add_argument('--output',type=Path)
    x=sp.add_parser('approve');x.add_argument('plan',type=Path);x.add_argument('--shots',required=True);x.add_argument('--confirmation',required=True)
    x=sp.add_parser('dry-run');x.add_argument('plan',type=Path);x.add_argument('--shot',action='append')
    x=sp.add_parser('generate');x.add_argument('plan',type=Path);x.add_argument('--output-dir',type=Path,default=Path('generated-broll'));x.add_argument('--approved',action='store_true');x.add_argument('--shot',action='append')
    x=sp.add_parser('roughcut');x.add_argument('plan',type=Path);x.add_argument('--source',type=Path,required=True);x.add_argument('--generated-dir',type=Path,required=True);x.add_argument('--output',type=Path,required=True);x.add_argument('--dry-run',action='store_true');x.add_argument('--generated-audio',choices=['sfx_only','mute'])
    x=sp.add_parser('probe');x.add_argument('media',type=Path)
    x=sp.add_parser('route-template');x.add_argument('text')
    a=p.parse_args()
    try:
        if a.cmd=='validate':
            e=validate_plan(load_plan(a.plan));print('VALID' if not e else '\n'.join('ERROR: '+x for x in e));return 0 if not e else 2
        if a.cmd=='review':
            s=review_markdown(load_plan(a.plan));(a.output.write_text(s+'\n',encoding='utf-8') if a.output else print(s));return 0
        if a.cmd=='approve':approve(a.plan,[x.strip() for x in a.shots.split(',') if x.strip()],a.confirmation);print('APPROVED');return 0
        if a.cmd=='dry-run':print(json.dumps(h3_adapter.run(a.plan,Path('generated-broll'),dry_run=True,requested=a.shot),ensure_ascii=False,indent=2));return 0
        if a.cmd=='generate':h3_adapter.run(a.plan,a.output_dir,approved=a.approved,requested=a.shot);return 0
        if a.cmd=='roughcut':
            r=roughcut.run(a.plan,a.source,a.generated_dir,a.output,dry_run=a.dry_run,generated_audio=a.generated_audio);print(json.dumps(r,ensure_ascii=False,indent=2) if a.dry_run else 'ROUGHCUT_WRITTEN');return 0
        if a.cmd=='probe':print(json.dumps(probe(a.media),ensure_ascii=False,indent=2));return 0
        if a.cmd=='route-template':print(json.dumps(template_router.recommend(a.text),ensure_ascii=False,indent=2));return 0
    except Exception as e:print('ERROR:',e,file=sys.stderr);return 2
if __name__=='__main__':raise SystemExit(main())
