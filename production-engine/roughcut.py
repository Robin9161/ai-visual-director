#!/usr/bin/env python3
from __future__ import annotations
import json, math, shutil, subprocess
from pathlib import Path
from plan_tool import load_plan, validate_plan
from media_probe import probe

def has_audio(m):return any(s.get('codec_type')=='audio' for s in m.get('streams',[]))
def video_size(m):
    for s in m.get('streams',[]):
        if s.get('codec_type')=='video':return int(s['width']),int(s['height'])
    raise ValueError('no video')
def clips(plan,generated_dir):
    seg_by={x.get('shot_id'):x for x in plan.get('segments',[]) if x.get('shot_id')};out=[]
    for s in plan.get('shots',[]):
        if s.get('approval')!='approved':continue
        g=seg_by.get(s.get('shot_id')); 
        if not g:continue
        a,b=g.get('start_sec'),g.get('end_sec')
        if not isinstance(a,(int,float)) or not isinstance(b,(int,float)) or b<=a:raise ValueError(f"invalid time for {s.get('shot_id')}")
        p=generated_dir/Path(s.get('output_name') or f"{s['shot_id']}.mp4").name
        if not p.is_file():continue
        out.append({'shot':s,'path':p,'start':float(a),'end':float(b)})
    out.sort(key=lambda x:x['start'])
    for x,y in zip(out,out[1:]):
        if y['start']<x['end']:raise ValueError('overlapping B-roll not supported by MVP roughcut')
    return out

def command(source,clips_,output,w,h,transition,generated_audio,gain_db):
    cmd=['ffmpeg','-y','-i',str(source)]
    for x in clips_:cmd += ['-stream_loop','-1','-i',str(x['path'])]
    filters=['[0:v]setpts=PTS-STARTPTS[v0]'];cur='v0';al=[];gain=math.pow(10,gain_db/20)
    for i,x in enumerate(clips_,1):
        a,b=x['start'],x['end'];dur=b-a;fade=min(transition,dur/3)
        filters.append(f'[{i}:v]trim=duration={dur:.6f},setpts=PTS-STARTPTS,scale={w}:{h}:force_original_aspect_ratio=increase,crop={w}:{h},format=rgba,fade=t=in:st=0:d={fade:.6f}:alpha=1,fade=t=out:st={max(0,dur-fade):.6f}:d={fade:.6f}:alpha=1,setpts=PTS+{a:.6f}/TB[bv{i}]')
        nxt=f'v{i}';filters.append(f"[{cur}][bv{i}]overlay=0:0:eof_action=pass:enable='between(t,{a:.6f},{b:.6f})'[{nxt}]");cur=nxt
        if generated_audio=='sfx_only' and has_audio(probe(x['path'])):
            delay=int(round(a*1000));filters.append(f'[{i}:a]atrim=duration={dur:.6f},asetpts=PTS-STARTPTS,volume={gain:.8f},adelay={delay}|{delay}[sfx{i}]');al.append(f'[sfx{i}]')
    if not has_audio(probe(source)):raise ValueError('source must have audio')
    filters.append('[0:a]asetpts=PTS-STARTPTS[voice]')
    if al:filters.append('[voice]'+''.join(al)+f'amix=inputs={1+len(al)}:duration=first:dropout_transition=0,alimiter=limit=0.95[aout]')
    else:filters.append('[voice]anull[aout]')
    cmd += ['-filter_complex',';'.join(filters),'-map',f'[{cur}]','-map','[aout]','-c:v','libx264','-preset','medium','-crf','17','-pix_fmt','yuv420p','-c:a','aac','-b:a','256k','-movflags','+faststart','-shortest',str(output)]
    return cmd

def run(plan_path,source,generated_dir,output,dry_run=False,generated_audio=None):
    if not shutil.which('ffmpeg') or not shutil.which('ffprobe'):raise RuntimeError('ffmpeg/ffprobe required')
    plan=load_plan(plan_path);e=validate_plan(plan)
    if e:raise ValueError('plan invalid: '+'; '.join(e))
    m=probe(source);w,h=video_size(m);c=clips(plan,generated_dir)
    if not c:raise ValueError('no approved generated clips')
    policy=generated_audio or plan['audio_policy'].get('generated_audio','sfx_only')
    cmd=command(source,c,output,w,h,float(plan.get('edit',{}).get('transition_sec',0.12)),policy,float(plan['audio_policy'].get('sfx_gain_db',-18)))
    if dry_run:return cmd
    output.parent.mkdir(parents=True,exist_ok=True);subprocess.run(cmd,check=True)
    man={'schema_version':'2.4','source':str(source),'output':str(output),'preserve_source_speech':True,'generated_audio':policy,'shots':[{'shot_id':x['shot']['shot_id'],'start_sec':x['start'],'end_sec':x['end'],'source':str(x['path'])} for x in c],'output_probe':probe(output)}
    output.with_name('edit-manifest.json').write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');return man
