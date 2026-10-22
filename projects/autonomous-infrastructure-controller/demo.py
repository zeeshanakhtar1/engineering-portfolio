"""Local proof-of-concept for autonomous-infrastructure-controller; not production-grade."""

def scale_decision(current, utilization, minimum=1, maximum=5):
    if not 0<=utilization<=1 or not minimum<=current<=maximum: raise ValueError('invalid state')
    delta=1 if utilization>.8 else -1 if utilization<.2 else 0
    return max(minimum,min(maximum,current+delta))

if __name__=='__main__':
    assert scale_decision(2,.9)==3
    assert scale_decision(1,.1)==1
    print('Controller tests passed')
