"""Cross-System Reliability Intelligence and Distributed Infrastructure Analytics: local-first domain-specific engine."""
def evaluate(data):
    graph=data['dependencies']; root=data['failed_service']
    impacted={root}
    while True:
        next_set=impacted|{name for name,deps in graph.items() if set(deps)&impacted}
        if next_set==impacted: break
        impacted=next_set
    return {'root_cause':root,'impacted_services':sorted(impacted),'blast_radius':len(impacted)}

