"""Intelligent Incident Diagnosis and Automated Infrastructure Remediation: local domain logic."""
def evaluate(data):
    rules={'disk_full':('inspect_disk','storage_team'),'high_latency':('collect_traces','sre_team'),'pod_crash':('inspect_pod_events','platform_team')}
    signal=data['signal']
    action,owner=rules.get(signal,('manual_triage','on_call'))
    approved=bool(data.get('approved',False))
    return {'signal':signal,'recommended_action':action,'owner':owner,'approval_recorded':approved,'executed':False,'requires_human':True}

