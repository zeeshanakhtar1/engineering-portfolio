import json
import threading
import unittest
from http.server import ThreadingHTTPServer
from urllib.request import urlopen
from app.main import Handler

class APITests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.base='http://127.0.0.1:%s' % cls.server.server_port

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()

    def test_health(self):
        with urlopen(self.base+'/healthz') as r:
            self.assertEqual(json.load(r)['status'],'alive')

    def test_readiness(self):
        with urlopen(self.base+'/readyz') as r:
            self.assertEqual(json.load(r)['status'],'ready')

    def test_info(self):
        with urlopen(self.base+'/api/v1/info') as r:
            self.assertEqual(json.load(r)['service'],'platform-example-api')

    def test_metrics(self):
        with urlopen(self.base+'/metrics') as r:
            self.assertIn('http_requests_total',r.read().decode())

if __name__=='__main__':
    unittest.main()
