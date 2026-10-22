"""Engineering Service Catalog and Software Architecture Governance: local domain logic."""
def evaluate(data):
    services=data['services']
    names=set(services)
    issues=[]
    for name,item in services.items():
        if not item.get('owner'):issues.append({'service':name,'issue':'missing_owner'})
        if name in item.get('depends_on',[]):issues.append({'service':name,'issue':'self_dependency'})
        for dep in item.get('depends_on',[]):
            if dep not in names:issues.append({'service':name,'issue':'unknown_dependency:'+dep})
    return {'valid':not issues,'service_count':len(services),'violations':issues}

