"""Threaded HTTP JSON ingest and local anomaly classification API."""
import json,os,math
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from threading import Lock
from .core import detect
from .store import MetricStore

class ApiServer(ThreadingHTTPServer):
    def __init__(self,address,db_path=':memory:'):
        super().__init__(address,ApiHandler)
        self.store=MetricStore(db_path)
        self.lock=Lock()
    def server_close(self):
        self.store.close()
        super().server_close()

class ApiHandler(BaseHTTPRequestHandler):
    def reply(self,status,payload):
        data=json.dumps(payload,allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(data)))
        self.end_headers()
        self.wfile.write(data)
    def do_GET(self):
        if self.path=='/healthz':
            self.reply(200,{'status':'ok'})
        elif self.path=='/metrics':
            with self.server.lock:
                count=self.server.store.db.execute('SELECT COUNT(*) FROM samples').fetchone()[0]
            self.reply(200,{'sample_count':count})
        else:
            self.reply(404,{'error':'not found'})
    def do_POST(self):
        if self.path!='/v1/ingest':
            return self.reply(404,{'error':'not found'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<=0 or size>4096:
                return self.reply(413,{'error':'request body must be 1-4096 bytes'})
            data=json.loads(self.rfile.read(size))
            metric=data['metric']; value=float(data['value'])
            if not isinstance(metric,str) or not metric.strip() or len(metric)>100:
                raise ValueError('metric must be non-empty string at most 100 chars')
            if not math.isfinite(value):
                raise ValueError('value must be finite')
            with self.server.lock:
                history=self.server.store.recent(metric)
                result=detect(metric,history,value)
                self.server.store.add(metric,value)
            self.reply(200,asdict(result))
        except (KeyError,ValueError,TypeError,json.JSONDecodeError) as exc:
            self.reply(400,{'error':str(exc)})
    def log_message(self,format,*args):
        return

def main():
    host=os.environ.get('AIOPS_HOST','127.0.0.1')
    port=int(os.environ.get('AIOPS_PORT','8091'))
    db=os.environ.get('AIOPS_DB','/tmp/aiops/metrics.sqlite3')
    server=ApiServer((host,port),db)
    try:
        print(f'AIOps API on {host}:{port}',flush=True)
        server.serve_forever()
    finally:
        server.server_close()

if __name__=='__main__':
    main()
