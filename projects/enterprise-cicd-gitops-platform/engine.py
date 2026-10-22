"""Enterprise CI/CD Automation and GitOps Delivery Platform: local domain logic."""
def evaluate(data):
    release=data['release']
    sha=release['git_sha']
    gates={'immutable_revision':len(sha)==40 and all(c in '0123456789abcdef' for c in sha.lower()),'tests':bool(release.get('tests_passed')),'security':bool(release.get('security_passed')),'approval':bool(release.get('approved')),'signed':bool(release.get('signed'))}
    return {'promote':all(gates.values()),'gates':gates,'revision':sha}

