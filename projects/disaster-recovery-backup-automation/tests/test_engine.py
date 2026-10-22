import json,unittest,sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from engine import evaluate
class EngineTests(unittest.TestCase):
    def test_scenario(self):
        with open(Path(__file__).resolve().parents[1]/'examples/scenario.json') as f:
            self.assertEqual(evaluate(json.load(f)),json.loads("{\"integrity_ok\":true,\"rpo_met\":true,\"rto_met\":true,\"sha256\":\"ba7816bf8f01cfea414140de5dae2223b00361a396177a9cb410ff61f20015ad\"}"))
    def test_result_is_object(self):
        with open(Path(__file__).resolve().parents[1]/'examples/scenario.json') as f:
            self.assertIsInstance(evaluate(json.load(f)),dict)
if __name__=='__main__':unittest.main()
