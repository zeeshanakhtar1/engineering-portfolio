"""High-signal source pattern scanner that never prints secret values."""
import argparse,json,re
from pathlib import Path

RULES={
    'private_key_header':re.compile(r'-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----'),
    'aws_access_key_candidate':re.compile(r'\b(?:AKIA|ASIA)[A-Z0-9]{16}\b'),
    'hardcoded_credential_assignment':re.compile(r'(?i)\b(?:api[_-]?key|secret[_-]?key|password)\s*[=:]\s*["\x27][^"\x27\s]{12,}["\x27]'),
}
IGNORED={'.git','.venv','venv','node_modules','__pycache__','.terraform','dist','build'}

def scan(root,max_bytes=1024*1024):
    root=Path(root).resolve()
    if not root.is_dir():raise ValueError('directory required')
    findings=[];checked=0
    for path in sorted(root.rglob('*')):
        if not path.is_file() or path.is_symlink() or any(part in IGNORED for part in path.relative_to(root).parts):continue
        if path.stat().st_size>max_bytes:continue
        try:text=path.read_text(encoding='utf-8')
        except (UnicodeDecodeError,OSError):continue
        checked+=1
        for line_no,line in enumerate(text.splitlines(),start=1):
            for rule,pattern in RULES.items():
                if pattern.search(line):
                    findings.append({'path':path.relative_to(root).as_posix(),'line':line_no,'rule':rule})
    return {'files_checked':checked,'findings':findings,'passed':not findings}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('path',nargs='?',default='.')
    options=parser.parse_args()
    result=scan(options.path)
    print(json.dumps(result,indent=2))
    raise SystemExit(0 if result['passed'] else 2)

if __name__=='__main__':main()
