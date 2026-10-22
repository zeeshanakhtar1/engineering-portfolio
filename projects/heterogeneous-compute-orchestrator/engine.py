"""Heterogeneous Computing and Adaptive Workload Orchestration: local domain logic."""
def evaluate(data):
    estimates=data['estimates']
    max_cost=float(data.get('max_cost',1e9))
    candidates=[e for e in estimates if e['duration_ms']>0 and e['estimated_cost']<=max_cost]
    if not candidates:return {'device':None,'eligible':0,'estimated_duration_ms':None}
    best=min(candidates,key=lambda x:(x['duration_ms'],x['estimated_cost'],x['device']))
    return {'device':best['device'],'eligible':len(candidates),'estimated_duration_ms':best['duration_ms']}

