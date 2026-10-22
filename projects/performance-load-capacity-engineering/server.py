import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from engine import evaluate
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_json(200,{'status':'healthy'}) if self.path=='/healthz' else self.send_json(404,{'error':'not_found'})
    def do_POST(self):
        if self.path!='/evaluate':return self.send_json(404,{'error':'not_found'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if n<=0 or n>32768:return self.send_json(413,{'error':'body_too_large'})
            return self.send_json(200,evaluate(json.loads(self.rfile.read(n))))
        except (KeyError,ValueError,TypeError,OverflowError) as e:return self.send_json(400,{'error':str(e)})
    def send_json(self,status,data):
        raw=json.dumps(data,allow_nan=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
    def log_message(self,*args):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.getenv('PORT','8080'))),Handler).serve_forever()
