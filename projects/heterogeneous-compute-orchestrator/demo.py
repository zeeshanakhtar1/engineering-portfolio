"""Local proof-of-concept for heterogeneous-compute-orchestrator; not production-grade."""

def choose_device(workload, estimates):
    eligible={k:v for k,v in estimates.get(workload,{}).items() if v>0}
    return min(eligible,key=eligible.get) if eligible else None

if __name__=='__main__':
    assert choose_device('matrix',{'matrix':{'cpu':10,'gpu':2}})=='gpu'
    print('Scheduling model passed')
