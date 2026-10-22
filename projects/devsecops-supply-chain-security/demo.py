"""DevSecOps and Software Supply Chain Security.

Reject artifacts with critical findings or missing attestations.
Local, dependency-free educational prototype; not production infrastructure.
"""

def artifact_policy(critical_vulnerabilities, has_sbom, signed):
    return critical_vulnerabilities==0 and has_sbom and signed

if __name__ == '__main__':
    assert artifact_policy(0,True,True)
    assert not artifact_policy(1,True,True)
    print('Artifact security checks passed')
