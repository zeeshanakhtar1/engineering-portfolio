"""Local proof-of-concept for post-quantum-tls-migration-readiness; not production-grade."""

def classify_tls(version, hybrid_supported, handshake_passed, application_passed):
    if version!='1.3': return 'requires_tls13_upgrade'
    if not hybrid_supported: return 'hybrid_group_unsupported'
    if not handshake_passed: return 'handshake_failed'
    if not application_passed: return 'application_validation_failed'
    return 'candidate_ready_for_performance_evaluation'

if __name__=='__main__':
    assert classify_tls('1.3',True,True,True)=='candidate_ready_for_performance_evaluation'
    print('Readiness rules passed')
