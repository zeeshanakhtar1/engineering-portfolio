"""Cryptographic Agility, Key Lifecycle and Security Policy Automation: local-first domain-specific engine."""
from datetime import date
def evaluate(data):
    forbidden=set(data.get('disallowed_algorithms',['SHA-1','RSA-1024','3DES']))
    flagged=[]; expiring=[]
    today=date.fromisoformat(data['as_of'])
    for entry in data['inventory']:
        if entry['algorithm'] in forbidden: flagged.append(entry['id'])
        if (date.fromisoformat(entry['expires_on'])-today).days<=30: expiring.append(entry['id'])
    return {'noncompliant_ids':sorted(flagged),'expiring_ids':sorted(expiring),'policy_passed':not flagged and not expiring}

