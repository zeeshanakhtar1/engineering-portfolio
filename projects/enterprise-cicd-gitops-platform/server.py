import json,os
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from engine import evaluate
class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.reply(200,{'status':'ok'}) if self.path=='/healthz' else self.reply(404,{'error':'not_found'})
    def do_POST(self):
        if self.path!='/evaluate':return self.reply(404,{'error':'not_found'})
        try:
            n=int(self.headers.get('Content-Length','0'))
            if not 0<n<=32768:return self.reply(413,{'error':'body_too_large'})
            self.reply(200,evaluate(json.loads(self.rfile.read(n))))
        except (ValueError,KeyError,TypeError,OverflowError) as e:self.reply(400,{'error':str(e)})
    def reply(self,status,value):
        data=json.dumps(value,allow_nan=False).encode()
        self.send_response(status);self.send_header('Content-Type','application/json');self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data)
    def log_message(self,*args):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.getenv('PORT','8080'))),Handler).serve_forever()
