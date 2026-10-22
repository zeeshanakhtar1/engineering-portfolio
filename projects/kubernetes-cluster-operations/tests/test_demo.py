import importlib.util
from pathlib import Path
import unittest

SPEC=importlib.util.spec_from_file_location('project_demo',Path(__file__).resolve().parents[1]/'demo.py')
module=importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(module)

class RolloutHealthTests(unittest.TestCase):
    def test_healthy(self):
        self.assertTrue(module.rollout_health(5,4,1)['healthy'])
    def test_unhealthy(self):
        self.assertFalse(module.rollout_health(5,3,1)['healthy'])
    def test_zero_desired(self):
        self.assertEqual(module.rollout_health(0,0)['availability'],1.0)

if __name__=='__main__':
    unittest.main()
