import math
"""Priority-aware GPU allocation: reserve GPUs for GPU-only workloads."""
def evaluate(data):
    nodes, jobs = data['nodes'], data['jobs']
    node_ids, job_ids = [n['id'] for n in nodes], [j['id'] for j in jobs]
    if len(set(node_ids)) != len(node_ids) or len(set(job_ids)) != len(job_ids):
        raise ValueError('duplicate node or job identifier')
    if any(not math.isfinite(float(x['memory_gb'])) or float(x['memory_gb']) <= 0 for x in [*nodes, *jobs]):
        raise ValueError('node and job memory must be finite and positive')
    jobs=sorted(data['jobs'],key=lambda j:(-int(j.get('priority',0)),j['id']))
    free={n['id']:{'memory_gb':float(n['memory_gb']),'gpu':bool(n.get('gpu'))} for n in data['nodes']}
    assigned={};pending=[]
    for job in jobs:
        needed=float(job['memory_gb'])
        eligible=[name for name,node in free.items() if node['memory_gb']>=needed and (not job.get('requires_gpu') or node['gpu'])]
        if not eligible:
            pending.append(job['id'])
            continue
        chosen=min(eligible,key=lambda n:(int(free[n]['gpu'] and not job.get('requires_gpu')),free[n]['memory_gb']-needed,n))
        assigned[job['id']]=chosen
        free[chosen]['memory_gb']-=needed
    return {'assigned':assigned,'pending':pending}
