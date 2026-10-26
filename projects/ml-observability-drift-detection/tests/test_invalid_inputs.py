import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_nan_observation_rejected(self):
        with self.assertRaises(ValueError): evaluate({'reference':[1,2],'current':[float('nan'),3]})
    def test_negative_threshold_rejected(self):
        with self.assertRaises(ValueError): evaluate({'reference':[1,2],'current':[2,3],'threshold':-1})

if __name__=='__main__': unittest.main()
