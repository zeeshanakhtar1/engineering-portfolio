"""Multi-Cloud Infrastructure Architecture and Deployment Orchestration local evaluation engine."""
def evaluate(data):
    workload=data['workload']
    limits=data['providers']
    supported=[p for p in limits if workload['cpu']<=p['cpu_limit'] and workload['memory_gb']<=p['memory_limit_gb']]
    recommended=min(supported,key=lambda p:(p['cost_score'],p['name']))['name'] if supported else None
    return {'candidate_providers':sorted(p['name'] for p in supported),'preferred':recommended,'deploy':False}

