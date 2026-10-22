"""GPU Workload Scheduling and AI Compute Resource Optimization: local domain logic."""
def evaluate(data):
    jobs=sorted(data['jobs'],key=lambda j:(-int(j.get('priority',0)),j['id']))
    free={n['id']:{'memory_gb':float(n['memory_gb']),'gpu':bool(n.get('gpu'))} for n in data['nodes']}
    assigned={};pending=[]
    for job in jobs:
        needed=float(job['memory_gb'])
        eligible=[name for name,node in free.items() if node['memory_gb']>=needed and (not job.get('requires_gpu') or node['gpu'])]
        if not eligible:pending.append(job['id']);continue
        chosen=min(eligible,key=lambda n:(free[n]['memory_gb']-needed,n))
        assigned[job['id']]=chosen
        free[chosen]['memory_gb']-=needed
    return {'assigned':assigned,'pending':pending}

