import json, os, time
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from threading import Lock
START=time.monotonic()
COUNT=0
LOCK=Lock()
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global COUNT
        with LOCK: COUNT+=1
        if self.path in ('/healthz','/readyz','/api/v1/info'):
            payload={'/healthz':{'status':'alive'},'/readyz':{'status':'ready'},'/api/v1/info':{'service':'platform-example-api','version':os.getenv('APP_VERSION','dev')}}[self.path]
            data=json.dumps(payload).encode();ctype='application/json';status=200
        elif self.path=='/metrics':
            data=('# TYPE http_requests_total counter\nhttp_requests_total %d\n# TYPE process_uptime_seconds gauge\nprocess_uptime_seconds %.3f\n'%(COUNT,time.monotonic()-START)).encode();ctype='text/plain; version=0.0.4';status=200
        else:
            data=b'{"error":"not found"}';ctype='application/json';status=404
        self.send_response(status);self.send_header('Content-Type',ctype);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def log_message(self,fmt,*args):
        print(json.dumps({'event':'request','message':fmt%args}),flush=True)
if __name__=='__main__':
    ThreadingHTTPServer(('0.0.0.0',int(os.getenv('PORT','8080'))),Handler).serve_forever()
