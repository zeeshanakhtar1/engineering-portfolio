import json,sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from engine import evaluate
class Tests(unittest.TestCase):
    def test_contract(self):
        with open(root/'examples/scenario.json') as f: data=json.load(f)
        self.assertEqual(evaluate(data),json.loads("{\"valid\":true,\"service_count\":2,\"violations\":[]}"))
    def test_deterministic(self):
        with open(root/'examples/scenario.json') as f: data=json.load(f)
        self.assertEqual(evaluate(data),evaluate(data))
if __name__=='__main__':unittest.main()
