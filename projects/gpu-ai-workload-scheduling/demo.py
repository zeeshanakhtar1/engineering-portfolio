"""GPU and AI Workload Scheduling.

Choose eligible simulated compute nodes without requiring a GPU.
Local, dependency-free educational prototype; not production infrastructure.
"""

def place_workload(nodes, requested_memory_gb, needs_gpu=False):
    eligible=[n for n in nodes if n['free_memory_gb']>=requested_memory_gb and (not needs_gpu or n['gpu'])]
    return min(eligible,key=lambda n:n['free_memory_gb'])['name'] if eligible else None

if __name__ == '__main__':
    assert place_workload([{'name':'cpu','free_memory_gb':8,'gpu':False}],4)=='cpu'
    assert place_workload([{'name':'cpu','free_memory_gb':8,'gpu':False}],4,True) is None
    print('Placement checks passed')
