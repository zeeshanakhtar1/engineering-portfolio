import threading,unittest
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from loadtest.runner import benchmark,percentiles

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200);self.end_headers();self.wfile.write(b'ok')
    def log_message(self,*args):pass

class BenchmarkTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ThreadingHTTPServer(('127.0.0.1',0),Handler)
        threading.Thread(target=cls.server.serve_forever,daemon=True).start()
        cls.url=f'http://127.0.0.1:{cls.server.server_port}/healthz'
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close()
    def test_benchmark(self):
        result=benchmark(self.url,10,2)
        self.assertEqual(result['requested'],10)
        self.assertEqual(result['failures'],0)
        self.assertGreater(result['throughput_rps'],0)
    def test_scope_restriction(self):
        with self.assertRaises(ValueError):benchmark('http://example.org/',10,1)
    def test_bounded_load(self):
        with self.assertRaises(ValueError):benchmark(self.url,10000000,1000)
    def test_percentile_nearest_rank(self):
        self.assertEqual(percentiles([10,20,30,40])['p95_ms'],40)
if __name__=='__main__':unittest.main()
