"""Measure real local TLS 1.3 X25519 versus X25519MLKEM768 handshakes."""
import argparse,json,re,socket,statistics,subprocess,tempfile,time
from pathlib import Path
BASELINE='X25519'
HYBRID='X25519MLKEM768'

def openssl_groups():
    result=subprocess.run(['openssl','list','-tls-groups'],capture_output=True,text=True,timeout=10)
    if result.returncode!=0:return []
    return [g for g in re.split(r'[:\s]+',result.stdout.strip()) if g]

def parse_result(output,expected_group):
    group=re.search(r'(?:Negotiated TLS1\.3 group:|Peer Temp Key:)\s*([^\s,]+)',output)
    return {'tls13':'Protocol version: TLSv1.3' in output,
            'verified':'Verification: OK' in output and 'Verified peername: localhost' in output,
            'negotiated_group':group.group(1) if group else None,
            'group_match':bool(group and group.group(1)==expected_group)}

def free_local_port():
    with socket.socket() as sock:
        sock.bind(('127.0.0.1',0))
        return sock.getsockname()[1]

def measure(rounds=3):
    if not 1<=rounds<=20:raise ValueError('rounds must be between 1 and 20')
    groups=openssl_groups()
    names={g.lower() for g in groups}
    if BASELINE.lower() not in names or HYBRID.lower() not in names:
        return {'supported':False,'reason':'OpenSSL TLS group X25519MLKEM768 unavailable','available_groups':groups}
    with tempfile.TemporaryDirectory(prefix='hybrid-tls-test-') as directory:
        work=Path(directory);key=work/'key.pem';cert=work/'certificate.pem'
        req=subprocess.run(['openssl','req','-x509','-newkey','rsa:2048','-nodes','-keyout',str(key),'-out',str(cert),'-subj','/CN=localhost','-addext','subjectAltName=DNS:localhost,IP:127.0.0.1','-days','1'],capture_output=True,text=True,timeout=20)
        if req.returncode!=0:raise RuntimeError('certificate generation failed: '+req.stderr[-500:])
        port=free_local_port()
        with open(work/'server.log','w') as log:
            server=subprocess.Popen(['openssl','s_server','-accept',f'127.0.0.1:{port}','-cert',str(cert),'-key',str(key),'-tls1_3','-www'],stdout=log,stderr=subprocess.STDOUT)
            try:
                for attempt in range(40):
                    try:
                        with socket.create_connection(('127.0.0.1',port),timeout=.1):break
                    except OSError:time.sleep(.1)
                else:raise RuntimeError('local TLS test server did not become ready')
                results={}
                for group in (BASELINE,HYBRID):
                    measurements=[]
                    for index in range(rounds):
                        start=time.perf_counter()
                        client=subprocess.run(['openssl','s_client','-connect',f'127.0.0.1:{port}','-servername','localhost','-CAfile',str(cert),'-verify_hostname','localhost','-tls1_3','-groups',group,'-brief'],input='\n',capture_output=True,text=True,timeout=12)
                        duration=round((time.perf_counter()-start)*1000,3)
                        parsed=parse_result(client.stdout+client.stderr,group)
                        if client.returncode!=0 or not all(parsed[k] for k in ('tls13','verified','group_match')):
                            raise RuntimeError('TLS validation failed for '+group+': '+repr(parsed))
                        measurements.append(duration)
                    results[group]={'success':True,'handshakes':rounds,'mean_wall_ms':round(statistics.mean(measurements),3),'min_wall_ms':min(measurements),'max_wall_ms':max(measurements),'negotiated_group':group}
                version=subprocess.run(['openssl','version'],capture_output=True,text=True,timeout=5).stdout.strip()
                return {'supported':True,'openssl_version':version,'certificate':'ephemeral RSA self-signed CA trusted for this test only','results':results,'note':'Exploratory local handshake measurements; do not generalize as production benchmarks.'}
            finally:
                server.terminate()
                try:server.wait(timeout=3)
                except subprocess.TimeoutExpired:server.kill();server.wait()

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--rounds',type=int,default=3)
    parser.add_argument('--output')
    options=parser.parse_args()
    result=measure(options.rounds)
    text=json.dumps(result,indent=2)
    if options.output:Path(options.output).write_text(text+'\n',encoding='utf-8')
    print(text)
    if not result['supported']:raise SystemExit(2)

if __name__=='__main__':main()
