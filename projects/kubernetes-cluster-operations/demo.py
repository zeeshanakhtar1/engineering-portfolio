"""Kubernetes Cluster Operations.

Assess deployment rollout availability.
Local, dependency-free educational prototype; not production infrastructure.
"""

def rollout_health(desired, ready, unavailable_limit=0):
    if min(desired, ready, unavailable_limit) < 0: raise ValueError('negative replicas')
    return {'healthy': ready >= max(0, desired-unavailable_limit), 'availability': ready/desired if desired else 1.0}

if __name__ == '__main__':
    assert rollout_health(5,4,1)['healthy']
    assert not rollout_health(5,3,1)['healthy']
    print('Rollout health checks passed')
