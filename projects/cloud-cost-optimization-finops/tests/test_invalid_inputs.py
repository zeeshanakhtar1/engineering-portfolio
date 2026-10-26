import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_nonfinite_cost_rejected(self):
        for key in ('hourly_rate','hours','budget','idle_fraction'):
            d={'hourly_rate':0.2,'hours':100,'budget':10,'idle_fraction':0.2}
            d[key]=float('nan')
            with self.subTest(key=key), self.assertRaises(ValueError): evaluate(d)

if __name__=='__main__': unittest.main()
