"""Full-Stack Observability Platform.

Calculate latency percentiles and error ratios.
Local, dependency-free educational prototype; not production infrastructure.
"""

def summarize_requests(latencies_ms, failures):
    if len(latencies_ms)!=len(failures) or not latencies_ms: raise ValueError('invalid telemetry')
    data=sorted(latencies_ms)
    p95=data[max(0, (95*len(data)+99)//100-1)]
    return {'p95_ms':p95, 'error_ratio':sum(bool(x) for x in failures)/len(failures)}

if __name__ == '__main__':
    assert summarize_requests([10,20,30,40],[False,False,True,False])['error_ratio']==0.25
    print('Telemetry checks passed')
