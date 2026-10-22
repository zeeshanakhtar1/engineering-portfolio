"""ML Observability and Drift Detection.

Detect mean shifts in reference and observed feature distributions.
Local, dependency-free educational prototype; not production infrastructure.
"""

def mean_shift(reference, observed, threshold):
    if not reference or not observed or threshold<0: raise ValueError('invalid sample')
    delta=abs(sum(reference)/len(reference)-sum(observed)/len(observed))
    return {'drift_detected':delta>threshold,'mean_shift':delta}

if __name__ == '__main__':
    assert mean_shift([1,1],[3,3],1)['drift_detected']
    print('Drift detection passed')
