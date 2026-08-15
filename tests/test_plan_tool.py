import json, tempfile, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'production-engine'))
from plan_tool import validate_plan,candidate_expected,approve,CONFIRMATION

ROOT=Path(__file__).resolve().parents[1]
class TestPlan(unittest.TestCase):
 def load(self):return json.loads((ROOT/'examples/ffmpeg-90s-plan.example.json').read_text(encoding='utf-8'))
 def test_example_valid(self):self.assertEqual(validate_plan(self.load()),[])
 def test_budget(self):self.assertEqual(candidate_expected('A','HERO'),3);self.assertEqual(candidate_expected('B','PRIMARY',True),2);self.assertEqual(candidate_expected('C','SUPPORT'),1)
 def test_blocker_fails_approval(self):
  p=self.load();p['script_blockers']=[{'severity':'BLOCKER','resolved':False}]
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'p.json';f.write_text(json.dumps(p,ensure_ascii=False),encoding='utf-8')
   with self.assertRaises(ValueError):approve(f,['B001'],CONFIRMATION)
 def test_missing_asset_fails_approval(self):
  p=self.load();p['asset_requests'][0]['status']='missing';p['asset_requests'][0]['resolved_path']=None
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'p.json';f.write_text(json.dumps(p,ensure_ascii=False),encoding='utf-8')
   with self.assertRaises(ValueError):approve(f,['B001'],CONFIRMATION)
 def test_keyframe_pending_fails_approval(self):
  p=self.load();p['shots'][0]['keyframe_gate']='PENDING'
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'p.json';f.write_text(json.dumps(p,ensure_ascii=False),encoding='utf-8')
   with self.assertRaises(ValueError):approve(f,['B001'],CONFIRMATION)
 def test_unlocked_world_fails_h3_approval(self):
  p=self.load();p['world']['status']='SELECTED'
  with tempfile.TemporaryDirectory() as d:
   f=Path(d)/'p.json';f.write_text(json.dumps(p,ensure_ascii=False),encoding='utf-8')
   with self.assertRaises(ValueError):approve(f,['B001'],CONFIRMATION)

if __name__=='__main__':unittest.main()
