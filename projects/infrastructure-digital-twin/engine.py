"""Infrastructure Digital Twin and Predictive Failure Simulation: local domain logic."""
def evaluate(data):
    graph=data['dependencies']; failed=set(data['failed'])
    timeline=[sorted(failed)]
    for step in range(len(graph)):
        newly={name for name,deps in graph.items() if set(deps)&failed}
        next_failed=failed|newly
        if next_failed==failed:break
        failed=next_failed;timeline.append(sorted(failed))
    return {'failed_services':sorted(failed),'propagation_steps':len(timeline)-1,'timeline':timeline}

