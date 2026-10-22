"""Post-Quantum Cryptography Migration Readiness and Hybrid TLS Validation local evaluation engine."""
def evaluate(data):
    checks={'tls13':data.get('tls_version')=='1.3','hybrid_supported':bool(data.get('hybrid_supported')),'interop':bool(data.get('interop_ok')),'application':bool(data.get('application_ok')),'performance':bool(data.get('performance_within_target'))}
    if not checks['tls13']:status='upgrade_tls_version'
    elif not checks['hybrid_supported']:status='enable_hybrid_group'
    elif not checks['interop']:status='investigate_handshake_failure'
    elif not checks['application']:status='investigate_application_functionality'
    elif not checks['performance']:status='optimize_performance'
    else:status='candidate_migration_ready'
    return {'readiness':status,'checks':checks,'validated_crypto':False,'evidence_type':'supplied_fixture_only'}

