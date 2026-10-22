"""Chaos Engineering and Automated Service Recovery: local-first domain-specific engine."""
def evaluate(data):
    nodes=int(data['nodes']); healthy=int(data['healthy']); faults=int(data['faults']); minimum=int(data['minimum_healthy'])
    if min(nodes,healthy,faults,minimum)<0 or healthy>nodes or faults>healthy or minimum>nodes: raise ValueError('invalid disruption scenario')
    remaining=healthy-faults
    allowed=remaining>=minimum
    return {'allowed':allowed,'healthy_after':remaining if allowed else healthy,'reason':'within_error_budget' if allowed else 'disruption_budget_exceeded','faults_applied':0}

