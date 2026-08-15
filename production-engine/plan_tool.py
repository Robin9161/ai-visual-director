#!/usr/bin/env python3
from __future__ import annotations
import json, re
from pathlib import Path

ROUTES={'A_ROLL','REAL_EVIDENCE','EXISTING_MEDIA','MOTION_GRAPHICS','H3_PACKAGING','H3_VIDEO','HYBRID'}
RENDER_MEDIA={'H3_VIDEO','KEYFRAME_MOTION','MOTION_GRAPHICS','REAL_REFERENCE','HYBRID','TALKING_HEAD'}
ROLES={'HERO','PRIMARY','SUPPORT'}
GRADES={'A','B','C'}
PRECISION={'NONE','POST_OVERLAY','SCREEN_REPLACE','SURFACE_TRACK'}
KEYFRAME={'PREVIEW','PRODUCTION','SKIP'}
APPROVAL={'pending','approved','rejected'}
CONFIRMATION='CONFIRM_H3_COST'
SECRET_KEYS=re.compile(r'(api[_-]?key|authorization|access[_-]?token|secret)',re.I)

def load_plan(path:Path)->dict:
    return json.loads(path.read_text(encoding='utf-8'))

def save_plan(path:Path, plan:dict):
    path.write_text(json.dumps(plan,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

def _secrets(v, trail='root'):
    out=[]
    if isinstance(v,dict):
        for k,c in v.items():
            if SECRET_KEYS.search(str(k)): out.append(f'{trail}.{k}')
            out+=_secrets(c,f'{trail}.{k}')
    elif isinstance(v,list):
        for i,c in enumerate(v): out+=_secrets(c,f'{trail}[{i}]')
    return out

def candidate_expected(grade,role,is_main=False):
    if grade=='A': return 3 if role=='HERO' or (role=='PRIMARY' and is_main) else 1
    if grade=='B': return 2 if role=='PRIMARY' and is_main else 1
    return 1

def blocking_assets(plan, shots):
    ids={s.get('shot_id') for s in shots}; segs={x.get('segment_id') for x in plan.get('segments',[]) if x.get('shot_id') in ids}
    out=[]
    for r in plan.get('asset_requests',[]):
        if r.get('status')!='missing' or r.get('blocks_generation') is not True: continue
        rs=set(r.get('shot_ids',[])); rg=set(r.get('segment_ids',[]))
        if (not rs and not rg) or rs&ids or rg&segs: out.append(r)
    return out

def unresolved_script_blockers(plan):
    return [b for b in plan.get('script_blockers',[]) if b.get('severity')=='BLOCKER' and not b.get('resolved')]

def validate_plan(plan:dict)->list[str]:
    e=[]
    for k in ['schema_version','project','source','world','approval','audio_policy','asset_requests','segments','shots']:
        if k not in plan:e.append(f'missing top-level field: {k}')
    if str(plan.get('schema_version'))!='2.4':e.append('schema_version must be 2.4')
    sec=_secrets(plan)
    if sec:e.append('credentials must not be stored in plan: '+', '.join(sec))
    world=plan.get('world',{})
    if world.get('status') not in {'DRAFT','SELECTED','LOCKED'}: e.append('world.status invalid')
    ap=plan.get('approval',{})
    if ap.get('status') not in {'pending','partially_approved','approved','rejected'}:e.append('approval.status invalid')
    aud=plan.get('audio_policy',{})
    if aud.get('music')!='forbidden':e.append('audio_policy.music must be forbidden')
    if aud.get('dialogue')!='forbidden':e.append('audio_policy.dialogue must be forbidden')
    if aud.get('preserve_source_speech') is not True:e.append('audio_policy.preserve_source_speech must be true')
    gain=aud.get('sfx_gain_db',-18)
    if not isinstance(gain,(int,float)) or not -36<=gain<=-6:e.append('audio_policy.sfx_gain_db must be -36..-6')
    shot_ids=set(); seg_ids=set()
    for i,s in enumerate(plan.get('segments',[])):
        sid=s.get('segment_id');
        if not sid:e.append(f'segments[{i}].segment_id missing')
        elif sid in seg_ids:e.append(f'duplicate segment_id: {sid}')
        seg_ids.add(sid)
        if s.get('route') not in ROUTES:e.append(f'segments[{i}].route invalid')
        a,b=s.get('start_sec'),s.get('end_sec')
        if a is not None or b is not None:
            if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or b<=a:e.append(f'segments[{i}] invalid timestamps')
    for i,s in enumerate(plan.get('shots',[])):
        p=f'shots[{i}]'; sid=s.get('shot_id')
        if not sid:e.append(f'{p}.shot_id missing')
        elif sid in shot_ids:e.append(f'duplicate shot_id: {sid}')
        shot_ids.add(sid)
        if s.get('grade') not in GRADES:e.append(f'{p}.grade invalid')
        if s.get('role') not in ROLES:e.append(f'{p}.role invalid')
        if s.get('render_medium') not in RENDER_MEDIA:e.append(f'{p}.render_medium invalid')
        if s.get('precision_mode') not in PRECISION:e.append(f'{p}.precision_mode invalid')
        if s.get('keyframe_mode') not in KEYFRAME:e.append(f'{p}.keyframe_mode invalid')
        if s.get('approval') not in APPROVAL:e.append(f'{p}.approval invalid')
        if not isinstance(s.get('prompt',''),str):e.append(f'{p}.prompt invalid')
        if s.get('render_medium') in {'H3_VIDEO','HYBRID'} and len(s.get('prompt',''))>2000:e.append(f'{p}.prompt >2000 chars')
        cc=s.get('candidate_count')
        exp=candidate_expected(s.get('grade'),s.get('role'),bool(s.get('is_main')))
        if cc!=exp:e.append(f'{p}.candidate_count should be {exp} by budget')
        if s.get('grade') in {'A','B'}:
            st=s.get('silent_test')
            if not isinstance(st,(int,float)):e.append(f'{p}.silent_test required')
            elif s.get('grade')=='A' and st<80:e.append(f'{p}.A silent_test <80')
            elif s.get('grade')=='B' and st<65:e.append(f'{p}.B silent_test <65')
        if s.get('precision_mode')!='NONE' and not s.get('precision'):
            e.append(f'{p}.precision details required')
        if s.get('keyframe_mode')=='PRODUCTION' and s.get('keyframe_gate') not in {'PASS','PENDING','RETURN'}:
            e.append(f'{p}.keyframe_gate required')
        if s.get('render_medium') in {'H3_VIDEO','HYBRID'}:
            ad=s.get('audio_design',{})
            if ad.get('music') is not False or ad.get('dialogue') is not False:e.append(f'{p}.audio_design music/dialogue must be false')
            if ad.get('generated_audio') not in {'sfx_only','mute'}:e.append(f'{p}.audio_design.generated_audio invalid')
    for r in plan.get('asset_requests',[]):
        if r.get('status') not in {'missing','provided','waived','not_needed'}:e.append(f"asset {r.get('request_id')} status invalid")
        if r.get('status')=='provided' and not r.get('resolved_path'):e.append(f"asset {r.get('request_id')} provided but no resolved_path")
    return e

def approval_gate_errors(plan:dict, shots:list[dict])->list[str]:
    e=[]
    if unresolved_script_blockers(plan): e.append('unresolved SCRIPT_BLOCKER')
    blocked=blocking_assets(plan,shots)
    if blocked:e.append('missing blocking assets: '+','.join(str(x.get('request_id')) for x in blocked))
    h3=[s for s in shots if s.get('render_medium') in {'H3_VIDEO','HYBRID'}]
    if h3 and plan.get('world',{}).get('status')!='LOCKED':e.append('world must be LOCKED before H3 approval')
    for s in h3:
        if s.get('keyframe_mode')=='PRODUCTION' and s.get('keyframe_gate')!='PASS':
            e.append(f"{s.get('shot_id')}: Production Keyframe gate must PASS before approval")
    return e

def approve(path:Path, shots:list[str], confirmation:str):
    if confirmation!=CONFIRMATION: raise ValueError('confirmation token mismatch')
    plan=load_plan(path)
    ve=validate_plan(plan)
    if ve: raise ValueError('plan invalid:\n- '+'\n- '.join(ve))
    known={s['shot_id']:s for s in plan.get('shots',[])}
    unknown=[x for x in shots if x not in known]
    if unknown: raise ValueError('unknown shots: '+','.join(unknown))
    selected=[known[x] for x in shots]
    ge=approval_gate_errors(plan,selected)
    if ge: raise ValueError('; '.join(ge))
    for x in shots: known[x]['approval']='approved'
    plan.setdefault('approval',{})['approved_shots']=sorted(set(plan.get('approval',{}).get('approved_shots',[]))|set(shots))
    plan['approval']['status']='approved' if set(plan['approval']['approved_shots'])==set(known) else 'partially_approved'
    save_plan(path,plan)
    return plan

def review_markdown(plan:dict)->str:
    lines=[f"# {plan.get('project',{}).get('name','AVD')} Review",'',f"World: {plan.get('world',{}).get('status')} {plan.get('world',{}).get('version','')}",'']
    bl=unresolved_script_blockers(plan)
    lines.append(f'Unresolved SCRIPT_BLOCKER: {len(bl)}'); lines.append('')
    for s in plan.get('shots',[]):
        lines += [f"## {s.get('shot_id')} — {s.get('short_name','')}",f"- Time: {s.get('start_sec')}–{s.get('end_sec')}",f"- Grade/Role: {s.get('grade')}/{s.get('role')}",f"- Render: {s.get('render_medium')}",f"- Template: {s.get('template_id','NONE')}",f"- Candidates: {s.get('candidate_count')}",f"- Precision: {s.get('precision_mode')}",f"- Approval: {s.get('approval')}",f"- Prompt: {s.get('prompt','')}",'']
    return '\n'.join(lines)
