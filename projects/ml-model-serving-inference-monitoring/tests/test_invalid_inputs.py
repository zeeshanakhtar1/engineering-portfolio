import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_nan_feature_rejected(self):
        with self.assertRaises(ValueError): evaluate({'weights':[1],'features':[float('nan')],'latency_ms':1})
    def test_negative_latency_rejected(self):
        with self.assertRaises(ValueError): evaluate({'weights':[1],'features':[2],'latency_ms':-1})

if __name__=='__main__': unittest.main()
