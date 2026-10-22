"""Machine Learning Observability, Data Drift and Model Performance Monitoring local evaluation engine."""
from statistics import mean
def evaluate(data):
    reference=[float(x) for x in data['reference']]
    current=[float(x) for x in data['current']]
    if not reference or not current:raise ValueError('datasets cannot be empty')
    delta=abs(mean(reference)-mean(current))
    threshold=float(data.get('threshold',1))
    return {'mean_reference':mean(reference),'mean_current':mean(current),'mean_shift':delta,'drift':delta>threshold,'retrain_recommended':delta>threshold}

