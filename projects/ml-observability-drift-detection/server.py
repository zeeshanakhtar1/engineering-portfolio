"""Bounded local HTTP adapter with explicit container host configuration."""
import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from engine import evaluate

class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        return self.respond(200,{'status':'ok'}) if self.path=='/healthz' else self.respond(404,{'error':'not_found'})
    def do_POST(self):
        if self.path!='/evaluate':return self.respond(404,{'error':'not_found'})
        try:
            length=int(self.headers.get('Content-Length','0'))
            if not 0<length<=32768:return self.respond(413,{'error':'request_body_limit'})
            result=evaluate(json.loads(self.rfile.read(length)))
            return self.respond(200,result)
        except (KeyError,ValueError,TypeError,OverflowError) as exc:
            return self.respond(400,{'error':str(exc)})
    def respond(self,status,payload):
        body=json.dumps(payload,allow_nan=False).encode()
        self.send_response(status)
        self.send_header('Content-Type','application/json')
        self.send_header('Content-Length',str(len(body)))
        self.end_headers()
        self.wfile.write(body)
    def log_message(self,*args):pass

if __name__=='__main__':
    ThreadingHTTPServer((os.getenv('HOST','127.0.0.1'),int(os.getenv('PORT','8080'))),Handler).serve_forever()
