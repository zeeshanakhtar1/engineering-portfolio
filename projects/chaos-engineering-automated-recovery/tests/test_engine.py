import json,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class EngineTests(unittest.TestCase):
    def test_scenario(self):
        with open(Path(__file__).resolve().parents[1]/'examples/scenario.json') as f:
            self.assertEqual(evaluate(json.load(f)),json.loads("{\"allowed\":false,\"healthy_after\":5,\"reason\":\"disruption_budget_exceeded\",\"faults_applied\":0}"))
    def test_result_is_object(self):
        with open(Path(__file__).resolve().parents[1]/'examples/scenario.json') as f:
            self.assertIsInstance(evaluate(json.load(f)),dict)
if __name__=='__main__':unittest.main()
