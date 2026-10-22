"""Cloud Infrastructure Landing Zone.

Validate network CIDR overlap and environment separation.
Local, dependency-free educational prototype; not production infrastructure.
"""

import ipaddress

def validate_networks(networks):
    parsed = [ipaddress.ip_network(n, strict=False) for n in networks]
    return {'valid': all(not a.overlaps(b) for i,a in enumerate(parsed) for b in parsed[i+1:]), 'networks': [str(n) for n in parsed]}

if __name__ == '__main__':
    assert validate_networks(['10.0.0.0/24','10.0.1.0/24'])['valid']
    assert not validate_networks(['10.0.0.0/24','10.0.0.128/25'])['valid']
    print('Network isolation checks passed')
