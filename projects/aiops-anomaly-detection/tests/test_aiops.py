import json,threading,unittest
from urllib.request import Request,urlopen
from aiops.core import detect
from aiops.store import MetricStore
from aiops.api import ApiServer

class DetectorTests(unittest.TestCase):
    def test_anomaly(self): self.assertTrue(detect('cpu',[9,10,11,9,10,11],100).anomalous)
    def test_normal(self): self.assertFalse(detect('cpu',[9,10,11,9,10,11],10).anomalous)
    def test_requires_history(self): self.assertEqual(detect('cpu',[10],100).reason,'insufficient_history')
    def test_constant_baseline(self): self.assertTrue(detect('cpu',[1]*5,2).anomalous)
    def test_bad_threshold(self):
        with self.assertRaises(ValueError): detect('cpu',[1]*5,10,threshold=0)
    def test_store_recent(self):
        db=MetricStore()
        try:
            for i in range(5): db.add('cpu',i)
            self.assertEqual(db.recent('cpu',3),[2,3,4])
            self.assertEqual(db.recent('mem'),[])
        finally: db.close()

class IntegrationTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server=ApiServer(('127.0.0.1',0))
        cls.thread=threading.Thread(target=cls.server.serve_forever,daemon=True)
        cls.thread.start()
        cls.url='http://127.0.0.1:%s'%cls.server.server_port
    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown();cls.server.server_close()
    def test_ingest(self):
        for i in range(6):
            body=json.dumps({'metric':'latency','value':10+i%2}).encode()
            with urlopen(Request(self.url+'/v1/ingest',body,{'Content-Type':'application/json'})) as r:
                self.assertEqual(r.status,200)
        body=b'{"metric":"latency","value":200}'
        with urlopen(Request(self.url+'/v1/ingest',body)) as r:
            self.assertTrue(json.load(r)['anomalous'])
    def test_health(self):
        with urlopen(self.url+'/healthz') as r:
            self.assertEqual(json.load(r)['status'],'ok')

if __name__=='__main__': unittest.main()
