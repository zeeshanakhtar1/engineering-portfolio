import json,sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from engine import evaluate
class ProjectTests(unittest.TestCase):
    def test_expected_result(self):
        with open(root/'examples/scenario.json') as f: sample=json.load(f)
        self.assertEqual(evaluate(sample),json.loads("{\"prediction\":12,\"latency_ms\":15,\"latency_slo_met\":true,\"feature_count\":2}"))
    def test_json_result(self):
        with open(root/'examples/scenario.json') as f: sample=json.load(f)
        self.assertIsInstance(json.dumps(evaluate(sample)),str)
if __name__=='__main__':unittest.main()
