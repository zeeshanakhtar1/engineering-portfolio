"""Policy-as-Code, Infrastructure Compliance and Multi-Tenant Security local evaluation engine."""
def evaluate(data):
    subject=data['subject'];resource=data['resource']
    allowed_actions={'reader':{'read'},'operator':{'read','restart'},'admin':{'read','restart','update'}}
    same_tenant=subject['tenant']==resource['tenant']
    role=subject['role'];action=data['action']
    authorized=same_tenant and action in allowed_actions.get(role,set())
    return {'permit':authorized,'same_tenant':same_tenant,'matched_role':role,'action':action,'deny_reason':None if authorized else ('cross_tenant' if not same_tenant else 'role_restriction')}

