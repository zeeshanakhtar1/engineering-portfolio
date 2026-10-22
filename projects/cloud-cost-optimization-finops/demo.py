"""Cloud Cost Optimization and Kubernetes FinOps.

Model projected spend and reject over-budget workloads.
Local, dependency-free educational prototype; not production infrastructure.
"""

def estimate_monthly_cost(hourly_rate, hours, budget=0):
    if min(hourly_rate,hours,budget)<0: raise ValueError('negative input')
    cost=round(hourly_rate*hours,2)
    return {'estimated_cost':cost,'within_budget':cost<=budget}

if __name__ == '__main__':
    assert estimate_monthly_cost(0,720)['within_budget']
    assert not estimate_monthly_cost(.1,720)['within_budget']
    print('Zero-cost guardrail passed')
