import json,sys,unittest
from pathlib import Path
root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from engine import evaluate
class Tests(unittest.TestCase):
    def test_contract(self):
        with open(root/'examples/scenario.json') as f: data=json.load(f)
        self.assertEqual(evaluate(data),json.loads("{\"promote\":false,\"gates\":{\"immutable_revision\":true,\"tests\":true,\"security\":true,\"approval\":false,\"signed\":true},\"revision\":\"aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa\"}"))
    def test_deterministic(self):
        with open(root/'examples/scenario.json') as f: data=json.load(f)
        self.assertEqual(evaluate(data),evaluate(data))
if __name__=='__main__':unittest.main()
