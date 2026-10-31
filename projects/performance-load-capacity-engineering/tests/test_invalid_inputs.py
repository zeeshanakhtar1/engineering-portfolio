import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_nonfinite_latency_rejected(self):
        with self.assertRaises(ValueError): evaluate({'latencies_ms':[1,float('nan')],'seconds':2,'capacity_rps':5})
    def test_infinite_duration_rejected(self):
        with self.assertRaises(ValueError): evaluate({'latencies_ms':[1],'seconds':float('inf'),'capacity_rps':5})

if __name__=='__main__': unittest.main()
