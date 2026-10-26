import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_nan_cpu_rejected(self):
        d={'request':{'environment':'dev','service':'api','cpu':float('nan'),'memory_gb':1,'owner':'platform'}}
        with self.assertRaises(ValueError): evaluate(d)

if __name__=='__main__': unittest.main()
