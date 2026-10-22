"""Bounded HTTP load generator for localhost-only endpoints."""
import argparse
from concurrent.futures import ThreadPoolExecutor,as_completed
import json,math,time
from urllib.parse import urlparse
from urllib.request import urlopen

def percentiles(values):
    values=sorted(values)
    if not values:raise ValueError('no observations')
    return {'p50_ms':values[math.ceil(len(values)*.50)-1],'p95_ms':values[math.ceil(len(values)*.95)-1],'p99_ms':values[math.ceil(len(values)*.99)-1]}

def sample(url,timeout):
    start=time.monotonic()
    try:
        with urlopen(url,timeout=timeout) as response:
            response.read(1024)
            status=response.status
    except Exception:
        status=0
    return {'latency_ms':round((time.monotonic()-start)*1000,3),'status':status}

def benchmark(url,total=20,concurrency=2,timeout=2):
    parts=urlparse(url)
    if parts.scheme!='http' or parts.hostname not in ('localhost','127.0.0.1','::1'):
        raise ValueError('only local endpoints may be load tested')
    if not 1<=total<=1000 or not 1<=concurrency<=16 or timeout<=0 or timeout>30:
        raise ValueError('unsafe benchmark bounds')
    started=time.monotonic()
    with ThreadPoolExecutor(max_workers=concurrency) as pool:
        futures=[pool.submit(sample,url,timeout) for _ in range(total)]
        results=[future.result() for future in as_completed(futures)]
    seconds=time.monotonic()-started
    latencies=[r['latency_ms'] for r in results]
    failures=sum(not 200<=r['status']<400 for r in results)
    return {'url':url,'requested':total,'failures':failures,'error_ratio':failures/total,'throughput_rps':round(total/seconds,3),'duration_seconds':round(seconds,3),**percentiles(latencies)}

def main():
    parser=argparse.ArgumentParser(description='Safe local HTTP benchmark')
    parser.add_argument('--url',default='http://127.0.0.1:8080/healthz')
    parser.add_argument('--requests',type=int,default=20)
    parser.add_argument('--concurrency',type=int,default=2)
    args=parser.parse_args()
    print(json.dumps(benchmark(args.url,args.requests,args.concurrency),indent=2))
if __name__=='__main__':main()
