import json, unittest, sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'production-engine'))
import h3_adapter
class TestDry(unittest.TestCase):
 def test_dryrun_payload(self):
  p=ROOT/'examples/ffmpeg-90s-plan.example.json'
  plan=json.loads(p.read_text(encoding='utf-8'));plan['shots'][0]['first_frame_image']='data:image/png;base64,AA=='
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   q=Path(d)/'p.json';q.write_text(json.dumps(plan,ensure_ascii=False),encoding='utf-8')
   out=h3_adapter.run(q,Path(d)/'out',dry_run=True)
   self.assertEqual(out[0]['shot_id'],'B001');self.assertEqual(out[0]['payload']['resolution'],'2K')

 def test_requested_shot_cannot_bypass_approval_for_real_run(self):
  p=ROOT/'examples/ffmpeg-90s-plan.example.json'
  plan=json.loads(p.read_text(encoding='utf-8'));plan['shots'][0]['first_frame_image']='data:image/png;base64,AA=='
  import tempfile
  with tempfile.TemporaryDirectory() as d:
   q=Path(d)/'p.json';q.write_text(json.dumps(plan,ensure_ascii=False),encoding='utf-8')
   with self.assertRaisesRegex(ValueError,'not approved'):
    h3_adapter.run(q,Path(d)/'out',approved=True,requested=['B001'])

if __name__=='__main__':unittest.main()
