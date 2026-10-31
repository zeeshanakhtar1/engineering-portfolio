import sys,unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class ValidationTests(unittest.TestCase):
    def test_invalid_recovery_times_rejected(self):
        for value in (-1,float('nan'),float('inf')):
            d={'backup_payload':'abc','data_loss_minutes':2,'rpo_target_minutes':5,'restore_minutes':value,'rto_target_minutes':30}
            with self.subTest(value=value), self.assertRaises(ValueError): evaluate(d)

if __name__=='__main__': unittest.main()
