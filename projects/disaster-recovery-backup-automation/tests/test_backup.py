import tempfile,unittest
from pathlib import Path
from dr.backup import snapshot,restore
class RecoveryTests(unittest.TestCase):
    def test_backup_restore_with_integrity(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);src=root/'source';(src/'sub').mkdir(parents=True)
            (src/'sub'/'config.json').write_text('{"version":1}')
            (src/'notes.txt').write_text('application data')
            backup=root/'snapshot.tar.gz'
            data=snapshot(src,backup)
            self.assertEqual(len(data['files']),2)
            response=restore(backup,root/'restored')
            self.assertTrue(response['verified'])
            self.assertEqual((root/'restored'/'notes.txt').read_text(),'application data')
    def test_tampered_backup_rejected(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'source').mkdir();(root/'source'/'a').write_text('secret')
            archive=root/'backup.tar.gz';snapshot(root/'source',archive)
            with archive.open('ab') as f:f.write(b'corrupt')
            with self.assertRaises(ValueError):restore(archive,root/'restored')
    def test_refuse_output_inside_source(self):
        with tempfile.TemporaryDirectory() as tmp:
            source=Path(tmp)
            with self.assertRaises(ValueError):snapshot(source,source/'backup.tar.gz')
    def test_never_overwrite_existing_target(self):
        with tempfile.TemporaryDirectory() as tmp:
            root=Path(tmp);(root/'source').mkdir();(root/'source'/'a').write_text('original')
            archive=root/'backup.tar.gz';snapshot(root/'source',archive)
            (root/'restore').mkdir();(root/'restore'/'a').write_text('existing')
            with self.assertRaises(ValueError):restore(archive,root/'restore')
if __name__=='__main__':unittest.main()
