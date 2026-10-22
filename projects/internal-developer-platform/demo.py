"""Internal Developer Platform.

Validate a developer self-service deployment request.
Local, dependency-free educational prototype; not production infrastructure.
"""

def provision_request(team, environment, cpu, memory_gb):
    allowed={'dev','test','staging'}
    return {'accepted':bool(team.strip()) and environment in allowed and 0<cpu<=4 and 0<memory_gb<=8}

if __name__ == '__main__':
    assert provision_request('platform','dev',2,4)['accepted']
    assert not provision_request('platform','production',2,4)['accepted']
    print('Self-service guardrails passed')
