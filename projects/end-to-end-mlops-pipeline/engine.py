"""End-to-End Machine Learning Pipeline and MLOps Automation: local-first domain-specific engine."""
from statistics import mean
def evaluate(data):
    train=[float(x) for x in data['train']]
    test=[float(x) for x in data['test']]
    if not train or not test: raise ValueError('datasets cannot be empty')
    prediction=mean(train)
    mae=mean([abs(x-prediction) for x in test])
    return {'model':'mean_baseline','prediction':prediction,'mae':mae,'train_samples':len(train),'test_samples':len(test)}

