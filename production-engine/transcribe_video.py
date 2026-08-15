#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,shutil,subprocess,sys
from pathlib import Path

def choose_backend():
    for name in ['openai_whisper','faster_whisper','mlx_whisper']:
        try:
            __import__({'openai_whisper':'whisper','faster_whisper':'faster_whisper','mlx_whisper':'mlx_whisper'}[name]);return name
        except Exception:pass
    return None

def probe_av(path):
    if not shutil.which('ffprobe'):raise RuntimeError('ffprobe required')
    out=json.loads(subprocess.run(['ffprobe','-v','error','-show_entries','stream=codec_type','-of','json',str(path)],check=True,capture_output=True,text=True).stdout)
    types={s.get('codec_type') for s in out.get('streams',[])}
    if 'video' not in types or 'audio' not in types:raise ValueError('input must contain video and audio')

def transcribe(path:Path,language='zh',model='small'):
    probe_av(path);b=choose_backend()
    if not b:raise RuntimeError('No whisper backend. Install openai-whisper, faster-whisper, or mlx-whisper.')
    seg=[]
    if b=='openai_whisper':
        import whisper;m=whisper.load_model(model);r=m.transcribe(str(path),language=language)
        seg=[{'start_sec':float(x['start']),'end_sec':float(x['end']),'text':x['text'].strip()} for x in r['segments']]
    elif b=='faster_whisper':
        from faster_whisper import WhisperModel;m=WhisperModel(model,device='cpu',compute_type='int8');it,_=m.transcribe(str(path),language=language);seg=[{'start_sec':float(x.start),'end_sec':float(x.end),'text':x.text.strip()} for x in it]
    else:
        import mlx_whisper;r=mlx_whisper.transcribe(str(path),path_or_hf_repo=f'mlx-community/whisper-{model}-mlx',language=language);seg=[{'start_sec':float(x['start']),'end_sec':float(x['end']),'text':x['text'].strip()} for x in r['segments']]
    return {'schema_version':'2.4','backend':b,'model':model,'language':language,'segments':seg}
