"""End-to-End MLOps Pipeline.

Train and evaluate a deterministic baseline predictor.
Local, dependency-free educational prototype; not production infrastructure.
"""

def train_mean_baseline(values):
    if not values: raise ValueError('empty training set')
    return sum(values)/len(values)

def mean_absolute_error(values, prediction):
    return sum(abs(v-prediction) for v in values)/len(values)

if __name__ == '__main__':
    model=train_mean_baseline([2,4,6])
    assert model==4 and mean_absolute_error([3,5],model)==1
    print('Baseline training and evaluation passed')
