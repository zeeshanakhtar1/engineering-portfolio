"""Full-Stack Observability, Monitoring and Distributed Tracing: local domain logic."""
import math
def evaluate(data):
    max_error = float(data.get('max_error_rate', .01))
    if not math.isfinite(max_error) or not 0 <= max_error <= 1:
        raise ValueError('max_error_rate must be between 0 and 1')
    items=data['requests']
    if not items:raise ValueError('requests required')
    ms=sorted(float(r['latency_ms']) for r in items)
    if any(x<0 or not math.isfinite(x) for x in ms):raise ValueError('invalid latency')
    idx=math.ceil(.95*len(ms))-1
    failed=sum(int(r.get('status',200))>=500 for r in items)
    return {'requests':len(items),'p95_ms':ms[idx],'error_rate':failed/len(items),'slo_violated':failed/len(items)>float(data.get('max_error_rate',.01))}

