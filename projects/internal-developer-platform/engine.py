"""Internal Developer Platform and Self-Service Infrastructure Provisioning: local domain logic."""
def evaluate(data):
    request=data['request'];environment=request['environment'];cpu=float(request['cpu']);ram=float(request['memory_gb'])
    reasons=[]
    if environment not in ('dev','test','staging'):reasons.append('environment_not_permitted')
    if cpu<=0 or cpu>4:reasons.append('cpu_limit')
    if ram<=0 or ram>8:reasons.append('memory_limit')
    if not request.get('owner'):reasons.append('missing_owner')
    return {'accepted':not reasons,'reasons':reasons,'resource_name':request['service']+'-'+environment,'provisioned':False}

