#!/usr/bin/env python3
from __future__ import annotations
import argparse, base64, json, mimetypes, os, time, urllib.request, urllib.error, urllib.parse
from datetime import datetime, timezone
from pathlib import Path
from plan_tool import load_plan, validate_plan, approval_gate_errors

def now(): return datetime.now(timezone.utc).isoformat()

def load_capabilities(root:Path)->dict:
    p=root.parent/'configs'/'h3_capabilities.json'
    if not p.exists(): p=root/'..'/'configs'/'h3_capabilities.json'
    return json.loads(Path(p).resolve().read_text(encoding='utf-8'))

def first_frame(v:str, plan_path:Path, caps:dict)->str:
    if v.startswith(('http://','https://','data:')): return v
    p=Path(v).expanduser(); p=p if p.is_absolute() else plan_path.parent/p
    if not p.is_file(): raise ValueError(f'first frame missing: {p}')
    if p.stat().st_size>caps.get('local_first_frame_max_mb',20)*1024*1024:raise ValueError('first frame too large')
    mime=mimetypes.guess_type(p.name)[0]
    if mime not in {'image/jpeg','image/png','image/webp'}:raise ValueError('unsupported first frame')
    return f'data:{mime};base64,'+base64.b64encode(p.read_bytes()).decode('ascii')

def payload_for(shot, plan, plan_path, caps):
    if shot.get('render_medium') not in {'H3_VIDEO','HYBRID'}: raise ValueError('shot is not H3 render medium')
    model=os.environ.get('MINIMAX_VIDEO_MODEL') or plan.get('api',{}).get('model') or caps['model_name']
    duration=int(shot.get('duration', plan.get('production',{}).get('duration',6)))
    resolution=shot.get('resolution', plan.get('production',{}).get('resolution','2K'))
    if resolution not in caps['resolutions']: raise ValueError(f'resolution not in capability: {resolution}')
    if not caps['duration_seconds_min']<=duration<=caps['duration_seconds_max']:raise ValueError('duration outside capability')
    content=[{'type':'text','text':shot['prompt']}]
    mode=shot.get('mode','text_to_video'); ratio=shot.get('ratio') or plan.get('project',{}).get('aspect_ratio','16:9')
    if mode=='image_to_video':
        content.append({'type':'image_url','image_url':{'url':first_frame(shot['first_frame_image'],plan_path,caps)},'role':'first_frame'}); ratio='adaptive'
    for item in shot.get('reference_media',[]):
        typ=item['type']; content.append({'type':typ,typ:{'url':item['url']},'role':item['role']}); ratio=shot.get('ratio','adaptive')
    return {'model':model,'content':content,'resolution':resolution,'duration':duration,'ratio':ratio,'aigc_watermark':bool(shot.get('aigc_watermark',False))}

def redact(v):
    if isinstance(v,str) and v.startswith('data:'):return '[base64 data URL omitted]'
    if isinstance(v,list):return [redact(x) for x in v]
    if isinstance(v,dict):return {k:redact(x) for k,x in v.items()}
    return v

def api(url,key,method='GET',payload=None):
    data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode()
    r=urllib.request.Request(url,data=data,method=method,headers={'Authorization':f'Bearer {key}','Content-Type':'application/json'})
    try:
        with urllib.request.urlopen(r,timeout=120) as x: body=x.read().decode()
    except urllib.error.HTTPError as e: raise RuntimeError(f'HTTP {e.code}: '+e.read().decode(errors='replace'))
    except urllib.error.URLError as e: raise RuntimeError(f'network: {e}')
    out=json.loads(body); br=out.get('base_resp')
    if isinstance(br,dict) and br.get('status_code',0)!=0:raise RuntimeError(json.dumps(out,ensure_ascii=False))
    return out

def selected_shots(plan, requested=None, dry_run=False):
    shots=[s for s in plan.get('shots',[]) if s.get('render_medium') in {'H3_VIDEO','HYBRID'}]
    if requested:
        wanted=set(requested); shots=[s for s in shots if s.get('shot_id') in wanted]
        missing=wanted-{s.get('shot_id') for s in shots}
        if missing: raise ValueError('unknown/non-H3 requested shots: '+','.join(sorted(missing)))
    elif not dry_run:
        ids=set(plan.get('approval',{}).get('approved_shots',[])); shots=[s for s in shots if s.get('shot_id') in ids and s.get('approval')=='approved']
    return shots

def require_real_generation_approval(plan, shots):
    approved_ids=set(plan.get('approval',{}).get('approved_shots',[]))
    not_approved=[s.get('shot_id') for s in shots if s.get('approval')!='approved' or s.get('shot_id') not in approved_ids]
    if not_approved:raise ValueError('shots are not approved: '+','.join(str(x) for x in not_approved))
    gate=approval_gate_errors(plan,shots)
    if gate:raise ValueError('; '.join(gate))

def run(plan_path:Path,outdir:Path,dry_run=False,approved=False,requested=None,poll=10,timeout=3600):
    plan=load_plan(plan_path); errs=validate_plan(plan)
    if errs: raise ValueError('plan invalid:\n- '+'\n- '.join(errs))
    caps=load_capabilities(Path(__file__).resolve().parent)
    shots=selected_shots(plan,requested,dry_run)
    if not shots: raise ValueError('no H3 shots selected')
    payloads=[(s,payload_for(s,plan,plan_path,caps)) for s in shots]
    if dry_run:return [{'shot_id':s['shot_id'],'submit_endpoint':caps['submit_path'],'payload':redact(p)} for s,p in payloads]
    if not approved:raise ValueError('real generation requires --approved')
    require_real_generation_approval(plan,shots)
    key=os.environ.get('MINIMAX_API_KEY')
    if not key:raise ValueError('MINIMAX_API_KEY not set')
    base=os.environ.get('MINIMAX_API_BASE') or plan.get('api',{}).get('base_url') or caps['base_url']; base=base.rstrip('/')
    outdir.mkdir(parents=True,exist_ok=True); manifest={'schema_version':'2.4','started_at':now(),'model':payloads[0][1]['model'],'shots':[]}
    mp=outdir/'generation-manifest.json'; mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    for shot,payload in payloads:
        rec={'shot_id':shot['shot_id'],'status':'submitting','payload':redact(payload),'started_at':now()};manifest['shots'].append(rec);mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        sub=api(base+caps['submit_path'],key,'POST',payload); task=str(sub.get('task_id') or '')
        if not task:raise RuntimeError('missing task_id')
        rec['task_id']=task; deadline=time.monotonic()+timeout
        while True:
            if time.monotonic()>deadline:raise RuntimeError(f'timeout: {task}')
            q=base+caps['query_path_template'].format(task_id=urllib.parse.quote(task,safe='')); status=api(q,key); t=status.get('task',status); st=str(t.get('status','')).lower();rec['status']=st;rec['last_status_response']=status;mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
            if st in {'success','succeeded'}:
                url=t.get('content',{}).get('url') or t.get('download_url');
                if not url:raise RuntimeError('success but no url')
                break
            if st in {'failed','failure','fail','cancelled'}:raise RuntimeError(json.dumps(status,ensure_ascii=False))
            time.sleep(max(1,poll))
        dest=outdir/Path(shot.get('output_name') or f"{shot['shot_id']}.mp4").name
        with urllib.request.urlopen(url,timeout=300) as r,dest.open('wb') as f:
            while True:
                b=r.read(1024*1024)
                if not b:break
                f.write(b)
        rec.update({'status':'downloaded','output':str(dest),'completed_at':now()});mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    manifest['completed_at']=now();mp.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return manifest
