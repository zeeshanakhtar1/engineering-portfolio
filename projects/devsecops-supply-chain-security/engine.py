"""DevSecOps Automation and Software Supply Chain Security: local-first domain-specific engine."""
def evaluate(data):
    violations=[]
    for artifact in data['artifacts']:
        missing=[key for key in ('sbom','signed','provenance') if not artifact.get(key,False)]
        if missing: violations.append({'artifact':artifact['name'],'controls':missing})
        if int(artifact.get('critical_vulnerabilities',0))>0:
            violations.append({'artifact':artifact['name'],'controls':['critical_vulnerabilities']})
    return {'passed':not violations,'violations':violations,'publish_allowed':not violations}

