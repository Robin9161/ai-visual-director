#!/usr/bin/env python3
import json, shutil, subprocess
from pathlib import Path

def probe(path:Path)->dict:
    if not shutil.which('ffprobe'):raise RuntimeError('ffprobe not installed')
    cmd=['ffprobe','-v','error','-show_entries','format=duration:stream=index,codec_type,codec_name,width,height,r_frame_rate','-of','json',str(path)]
    return json.loads(subprocess.run(cmd,check=True,capture_output=True,text=True).stdout)
