import math
"""Distributed Application Performance, Load and Capacity Engineering local evaluation engine."""
from statistics import mean
import math
def evaluate(data):
    values = [float(x) for x in data['latencies_ms']] + [float(data['seconds']),float(data['capacity_rps'])]
    if not all(math.isfinite(x) for x in values) or float(data['capacity_rps']) < 0:
        raise ValueError('benchmark values must be finite and capacity nonnegative')
    observations=[float(x) for x in data['latencies_ms']]
    if not observations or any(x<0 for x in observations) or float(data['seconds'])<=0:raise ValueError('invalid benchmark')
    ordered=sorted(observations)
    p95=ordered[math.ceil(.95*len(ordered))-1]
    rate=len(observations)/float(data['seconds'])
    return {'requests':len(observations),'throughput_rps':rate,'mean_latency_ms':mean(observations),'p95_latency_ms':p95,'below_capacity':rate<=float(data['capacity_rps'])}

