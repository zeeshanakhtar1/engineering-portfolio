"""Local-only HTTP entrypoint to this project's engine."""
import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from engine import evaluate
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.reply(200,{'status':'ok'}) if self.path=='/healthz' else self.reply(404,{'error':'not_found'})
    def do_POST(self):
        if self.path!='/evaluate':return self.reply(404,{'error':'not_found'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=32768: return self.reply(413,{'error':'body_too_large'})
            data=json.loads(self.rfile.read(size))
            self.reply(200,evaluate(data))
        except (ValueError,TypeError,KeyError,OverflowError) as exc:
            self.reply(400,{'error':str(exc)})
    def reply(self,status,data):
        payload=json.dumps(data,allow_nan=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(payload)));self.end_headers();self.wfile.write(payload)
    def log_message(self,*args):pass
if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',int(os.getenv('PORT','8080'))),Handler).serve_forever()
