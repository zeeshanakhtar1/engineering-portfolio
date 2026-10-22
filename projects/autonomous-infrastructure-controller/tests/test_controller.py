import json,tempfile,unittest
from pathlib import Path
from controller.engine import Policy,decide,AuditLog

class ControllerTests(unittest.TestCase):
    def test_scale_out(self):self.assertEqual(decide(2,.90,100).replicas_after,3)
    def test_scale_in(self):self.assertEqual(decide(3,.1,100).replicas_after,2)
    def test_max_bound(self):self.assertEqual(decide(5,.99,100).replicas_after,5)
    def test_min_bound(self):self.assertEqual(decide(1,.1,100).replicas_after,1)
    def test_cooldown(self):self.assertEqual(decide(2,.99,5).reason,'cooldown')
    def test_never_execute(self):self.assertFalse(decide(2,.99,100).execute)
    def test_invalid_utilization(self):
        with self.assertRaises(ValueError):decide(2,1.3,100)
    def test_audit(self):
        with tempfile.TemporaryDirectory() as d:
            path=Path(d)/'audit.jsonl'
            AuditLog(path).append(decide(2,.9,100))
            self.assertEqual(json.loads(path.read_text())['action'],'scale_out')

if __name__=='__main__':unittest.main()
