"""Local proof-of-concept for infrastructure-digital-twin; not production-grade."""

def impacted_services(dependencies, failed):
    impacted=set(failed)
    while True:
        expanded=impacted|{service for service,deps in dependencies.items() if set(deps)&impacted}
        if expanded==impacted: return sorted(impacted)
        impacted=expanded

if __name__=='__main__':
    assert impacted_services({'api':['db'],'web':['api']},['db'])==['api','db','web']
    print('Dependency simulation passed')
