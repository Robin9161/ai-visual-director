import unittest,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'production-engine'))
from template_router import recommend
class T(unittest.TestCase):
 def test_mechanism(self):self.assertTrue(any(x['id']=='T21' for x in recommend('解释视频编码机制和内部原理')))
 def test_compare(self):self.assertTrue(any(x['id']=='T14' for x in recommend('对比两个系统的差异')))
if __name__=='__main__':unittest.main()
