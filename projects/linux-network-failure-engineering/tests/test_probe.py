import threading,unittest
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from netdiag.probe import probe

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200);self.end_headers();self.wfile.write(b'ok')
    def log_message(self,*args):pass

class NetworkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close()
    def test_reachable_http(self):
        result=probe('127.0.0.1',self.server.server_port)
        self.assertTrue(result['healthy'])
        self.assertEqual([x['stage'] for x in result['stages']],['dns','tcp','http'])
    def test_closed_port(self):
        result=probe('127.0.0.1',1,timeout=.2)
        self.assertEqual(result['stages'][-1]['stage'],'tcp')
        self.assertFalse(result['healthy'])
    def test_invalid_timeout(self):
        with self.assertRaises(ValueError):probe('127.0.0.1',80,timeout=-1)

if __name__=='__main__':unittest.main()
