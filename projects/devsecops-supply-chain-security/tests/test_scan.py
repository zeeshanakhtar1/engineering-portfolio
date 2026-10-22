import tempfile,unittest
from pathlib import Path
from security.scan import scan

class ScannerTests(unittest.TestCase):
    def test_private_key_detected_without_leaking_contents(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'key.txt').write_text('-----BEGIN PRIVATE KEY-----\nPLACEHOLDER\n')
            result=scan(d)
            self.assertFalse(result['passed'])
            self.assertEqual(result['findings'][0]['rule'],'private_key_header')
            self.assertNotIn('PLACEHOLDER',str(result))
    def test_safe_file(self):
        with tempfile.TemporaryDirectory() as d:
            (Path(d)/'main.py').write_text('print("hello")\n')
            self.assertTrue(scan(d)['passed'])
    def test_ignored_directory(self):
        with tempfile.TemporaryDirectory() as d:
            directory=Path(d)/'node_modules';directory.mkdir()
            (directory/'foo').write_text('-----BEGIN PRIVATE KEY-----')
            self.assertTrue(scan(d)['passed'])
    def test_invalid_path(self):
        with self.assertRaises(ValueError):scan('/path-that-does-not-exist-security-test')
if __name__=='__main__':unittest.main()
