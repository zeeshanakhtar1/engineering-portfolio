"""Generate self-contained local service projects without cloud dependencies."""
import argparse,json,re
from pathlib import Path
NAME_PATTERN=re.compile(r'^[a-z][a-z0-9-]{1,38}[a-z0-9]$')

def scaffold(name,owner,directory):
    if not isinstance(name,str) or not NAME_PATTERN.fullmatch(name) or '--' in name:
        raise ValueError('service name must be lower-case kebab-case, 3-40 characters')
    if not isinstance(owner,str) or not owner.strip():
        raise ValueError('an accountable service owner is required')
    target=Path(directory).resolve()/name
    if target.exists():raise FileExistsError('service already exists; refusing to overwrite')
    target.mkdir(parents=True)
    (target/'app').mkdir()
    (target/'app'/'__init__.py').write_text('',encoding='utf-8')
    (target/'app'/'main.py').write_text('from http.server import BaseHTTPRequestHandler, HTTPServer\nimport os\nclass Handler(BaseHTTPRequestHandler):\n    def do_GET(self):\n        self.send_response(200 if self.path=="/healthz" else 404)\n        self.end_headers()\n        self.wfile.write(b"ok")\nif __name__=="__main__":HTTPServer(("0.0.0.0",int(os.getenv("PORT","8080"))),Handler).serve_forever()\n',encoding='utf-8')
    (target/'Dockerfile').write_text('FROM python:3.12-alpine\nWORKDIR /app\nCOPY app ./app\nRUN addgroup -S app && adduser -S -G app -u 10001 app\nUSER 10001\nEXPOSE 8080\nCMD ["python","-m","app.main"]\n',encoding='utf-8')
    (target/'compose.yaml').write_text('services:\n  api:\n    build: .\n    ports: ["127.0.0.1:8080:8080"]\n    read_only: true\n',encoding='utf-8')
    (target/'service.json').write_text(json.dumps({'name':name,'owner':owner,'status':'scaffold','runtime':'python3'},indent=2),encoding='utf-8')
    (target/'README.md').write_text(f'# {name}\n\nOwner: {owner}\n\nRun: `python3 -m app.main` or `docker compose up --build`.\n\nGET `/healthz` returns `ok`.\n',encoding='utf-8')
    return {'name':name,'path':str(target),'files':6}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--name',required=True)
    parser.add_argument('--owner',required=True)
    parser.add_argument('--output',default='./generated')
    args=parser.parse_args()
    print(json.dumps(scaffold(args.name,args.owner,args.output),indent=2))

if __name__=='__main__':main()
