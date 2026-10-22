"""Local proof-of-concept for cross-system-reliability-intelligence; not production-grade."""

def correlate(incidents, dependency):
    return sorted(i['service'] for i in incidents if dependency in i.get('dependencies',[]))

if __name__=='__main__':
    assert correlate([{'service':'api','dependencies':['db']}],'db')==['api']
    print('Correlation passed')
