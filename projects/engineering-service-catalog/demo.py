"""Engineering Service Catalog and Architecture Governance.

Validate service ownership and dependency references.
Local, dependency-free educational prototype; not production infrastructure.
"""

def validate_catalog(services):
    names=set(services)
    return {name: bool(item.get('owner')) and set(item.get('dependencies',[]))<=names and name not in item.get('dependencies',[]) for name,item in services.items()}

if __name__ == '__main__':
    assert validate_catalog({'api':{'owner':'platform','dependencies':[]}})['api']
    print('Catalog validation passed')
