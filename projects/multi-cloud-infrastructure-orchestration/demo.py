"""Multi-Cloud Infrastructure Orchestration.

Normalize cloud provider capacity descriptors.
Local, dependency-free educational prototype; not production infrastructure.
"""

def normalize_instance(provider, vcpu, memory_gb):
    if provider not in ('aws','azure','local') or vcpu<=0 or memory_gb<=0: raise ValueError('unsupported configuration')
    return {'provider':provider,'vcpu':vcpu,'memory_gb':memory_gb,'portable':True}

if __name__ == '__main__':
    assert normalize_instance('local',2,4)['portable']
    print('Provider normalization passed')
