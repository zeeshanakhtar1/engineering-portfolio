"""Linux Systems, Network Diagnostics and Failure Engineering local evaluation engine."""
def evaluate(data):
    checks=data['checks']; failures=[]
    for stage in ('dns','tcp','tls','http'):
        if not checks.get(stage,False):
            failures.append(stage)
            return {'healthy':False,'failure_stage':stage,'completed_checks':[x for x in ('dns','tcp','tls','http') if x not in failures and list(('dns','tcp','tls','http')).index(x)<list(('dns','tcp','tls','http')).index(stage)],'diagnosis':{'dns':'name_resolution','tcp':'transport_connectivity','tls':'tls_handshake','http':'application_response'}[stage]}
    return {'healthy':True,'failure_stage':None,'completed_checks':['dns','tcp','tls','http'],'diagnosis':'all_checks_passed'}

