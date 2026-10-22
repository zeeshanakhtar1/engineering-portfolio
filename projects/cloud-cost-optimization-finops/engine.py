"""Cloud Cost Optimization and Kubernetes FinOps: local-first domain-specific engine."""
def evaluate(data):
    hourly=float(data['hourly_rate']); hours=float(data['hours']); budget=float(data.get('budget',0)); idle=float(data.get('idle_fraction',0))
    if min(hourly,hours,budget)<0 or not 0<=idle<=1: raise ValueError('invalid cost inputs')
    baseline=round(hourly*hours,2)
    optimized=round(baseline*(1-idle),2)
    return {'baseline':baseline,'optimized':optimized,'potential_savings':round(baseline-optimized,2),'within_budget':optimized<=budget,'deploy':False}

