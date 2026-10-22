"""Policy-as-Code and Multi-Tenant Governance.

Enforce tenant isolation in simulated resource access.
Local, dependency-free educational prototype; not production infrastructure.
"""

def allow_access(identity_tenant, resource_tenant, action, allowed_actions=('read',)):
    return identity_tenant==resource_tenant and action in allowed_actions

if __name__ == '__main__':
    assert allow_access('a','a','read')
    assert not allow_access('a','b','read')
    print('Tenant isolation checks passed')
