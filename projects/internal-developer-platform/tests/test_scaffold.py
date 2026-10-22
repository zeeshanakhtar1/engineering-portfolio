import json,tempfile,unittest
from pathlib import Path
from idp.scaffold import scaffold

class ScaffoldTests(unittest.TestCase):
    def test_creates_service_package(self):
        with tempfile.TemporaryDirectory() as d:
            result=scaffold('billing-api','platform-team',d)
            folder=Path(result['path'])
            self.assertTrue((folder/'Dockerfile').is_file())
            self.assertEqual(json.loads((folder/'service.json').read_text())['owner'],'platform-team')
            self.assertTrue((folder/'app'/'main.py').is_file())
    def test_rejects_traversal(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):scaffold('../secrets','owner',d)
    def test_requires_owner(self):
        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(ValueError):scaffold('billing-api',' ',d)
    def test_refuses_overwrite(self):
        with tempfile.TemporaryDirectory() as d:
            scaffold('billing-api','team',d)
            with self.assertRaises(FileExistsError):scaffold('billing-api','team',d)
if __name__=='__main__':unittest.main()
