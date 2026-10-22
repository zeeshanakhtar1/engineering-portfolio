"""Performance Load and Capacity Engineering.

Estimate throughput and utilization from benchmark observations.
Local, dependency-free educational prototype; not production infrastructure.
"""

def capacity(completed_requests, duration_seconds, peak_rps):
    if duration_seconds<=0 or peak_rps<=0: raise ValueError('invalid capacity')
    rps=completed_requests/duration_seconds
    return {'throughput_rps':rps,'utilization':rps/peak_rps}

if __name__ == '__main__':
    assert capacity(1000,10,200)['utilization']==0.5
    print('Capacity calculations passed')
