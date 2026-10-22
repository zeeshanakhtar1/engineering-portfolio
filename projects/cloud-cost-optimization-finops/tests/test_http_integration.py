"""Loopback HTTP API integration tests for the standalone local evaluator."""
import json,sys,threading,unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.error import HTTPError

root=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(root))
from server import Handler
from engine import evaluate

class HTTPIntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.base='http://127.0.0.1:%s'%cls.server.server_port
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
    def test_health(self):
        with urlopen(self.base+'/healthz',timeout=3) as response:
            self.assertEqual(response.status,200)
            self.assertEqual(json.load(response)['status'],'ok')
    def test_evaluate(self):
        with open(root/'examples/scenario.json') as f:example=json.load(f)
        request=Request(self.base+'/evaluate',json.dumps(example).encode(),{'Content-Type':'application/json'})
        with urlopen(request,timeout=3) as response:
            self.assertEqual(response.status,200)
            self.assertEqual(json.load(response),evaluate(example))
    def test_reject_bad_json(self):
        request=Request(self.base+'/evaluate',b'{malformed',{'Content-Type':'application/json'})
        with self.assertRaises(HTTPError) as error:
            urlopen(request,timeout=3)
        self.assertEqual(error.exception.code,400)

if __name__=='__main__':unittest.main()
