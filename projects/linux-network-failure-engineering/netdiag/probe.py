"""Live DNS, TCP, optional TLS, and HTTP connectivity checks."""
import argparse,json,socket,ssl
from urllib.request import urlopen

def probe(host,port=80,protocol='http',timeout=2):
    if timeout<=0 or timeout>30 or not 0<port<=65535:raise ValueError('invalid probe settings')
    results=[]
    try:
        addresses=sorted({entry[4][0] for entry in socket.getaddrinfo(host,port,type=socket.SOCK_STREAM)})
        results.append({'stage':'dns','ok':True,'addresses':addresses})
    except OSError as exc:
        return {'healthy':False,'stages':[{'stage':'dns','ok':False,'error':str(exc)}]}
    try:
        with socket.create_connection((host,port),timeout=timeout):pass
        results.append({'stage':'tcp','ok':True})
    except OSError as exc:
        results.append({'stage':'tcp','ok':False,'error':str(exc)})
        return {'healthy':False,'stages':results}
    if protocol=='https':
        try:
            with socket.create_connection((host,port),timeout=timeout) as sock:
                with ssl.create_default_context().wrap_socket(sock,server_hostname=host) as tls:
                    results.append({'stage':'tls','ok':True,'version':tls.version()})
        except (ssl.SSLError,OSError) as exc:
            results.append({'stage':'tls','ok':False,'error':str(exc)})
            return {'healthy':False,'stages':results}
    elif protocol!='http':
        raise ValueError('protocol must be http or https')
    try:
        with urlopen(f'{protocol}://{host}:{port}/healthz',timeout=timeout) as response:
            status=response.status
        results.append({'stage':'http','ok':200<=status<400,'status':status})
    except Exception as exc:
        results.append({'stage':'http','ok':False,'error':str(exc)})
    return {'healthy':all(stage['ok'] for stage in results),'stages':results}

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('host',nargs='?',default='127.0.0.1')
    parser.add_argument('--port',type=int,default=8080)
    parser.add_argument('--protocol',choices=['http','https'],default='http')
    args=parser.parse_args()
    print(json.dumps(probe(args.host,args.port,args.protocol),indent=2))

if __name__=='__main__':main()
