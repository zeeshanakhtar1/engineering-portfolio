"""Chaos Engineering and Automated Recovery.

Check fault injection against a safe disruption budget.
Local, dependency-free educational prototype; not production infrastructure.
"""

def disruption_allowed(total, healthy, proposed_failures, min_available):
    if min(total,healthy,proposed_failures,min_available)<0 or healthy>total: raise ValueError('invalid state')
    return healthy-proposed_failures>=min_available

if __name__ == '__main__':
    assert disruption_allowed(5,5,1,4)
    assert not disruption_allowed(5,4,1,4)
    print('Chaos safety checks passed')
