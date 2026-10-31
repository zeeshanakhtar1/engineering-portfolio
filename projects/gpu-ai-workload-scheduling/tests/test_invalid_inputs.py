import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_duplicate_job_ids_rejected(self):
        d={'nodes':[{'id':'gpu','memory_gb':8,'gpu':True}], 'jobs':[{'id':'same','memory_gb':2},{'id':'same','memory_gb':3}]}
        with self.assertRaises(ValueError): evaluate(d)
    def test_negative_memory_rejected(self):
        d={'nodes':[{'id':'gpu','memory_gb':-8,'gpu':True}], 'jobs':[{'id':'a','memory_gb':2}]}
        with self.assertRaises(ValueError): evaluate(d)

if __name__=='__main__': unittest.main()
