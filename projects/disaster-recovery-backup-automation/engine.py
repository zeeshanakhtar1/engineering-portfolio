import math
"""Disaster Recovery, Backup Automation and Business Continuity: local-first domain-specific engine."""
from hashlib import sha256
def evaluate(data):
    durations = [float(data[k]) for k in ('data_loss_minutes', 'rpo_target_minutes', 'restore_minutes', 'rto_target_minutes')]
    if not all(math.isfinite(x) and x >= 0 for x in durations):
        raise ValueError('RPO/RTO measurements and targets must be finite and nonnegative')
    payload=data['backup_payload'].encode()
    digest=sha256(payload).hexdigest()
    restored=bytes.fromhex(data.get('restored_hex',payload.hex()))
    return {'integrity_ok':sha256(restored).hexdigest()==digest,'rpo_met':float(data['data_loss_minutes'])<=float(data['rpo_target_minutes']),'rto_met':float(data['restore_minutes'])<=float(data['rto_target_minutes']),'sha256':digest}

