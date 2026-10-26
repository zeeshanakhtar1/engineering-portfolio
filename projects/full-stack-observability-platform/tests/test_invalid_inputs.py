import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_invalid_slo_rejected(self):
        for limit in (-1,2,float('nan')):
            with self.subTest(limit=limit), self.assertRaises(ValueError): evaluate({'requests':[{'latency_ms':5,'status':200}], 'max_error_rate':limit})

if __name__=='__main__': unittest.main()
