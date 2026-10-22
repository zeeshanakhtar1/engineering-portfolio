"""Linux and Network Failure Engineering.

Classify common connectivity failures.
Local, dependency-free educational prototype; not production infrastructure.
"""

def diagnose(dns_ok, tcp_ok, tls_ok):
    if not dns_ok: return 'dns_resolution'
    if not tcp_ok: return 'transport_connectivity'
    if not tls_ok: return 'tls_handshake'
    return 'healthy'

if __name__ == '__main__':
    assert diagnose(True,False,False)=='transport_connectivity'
    print('Network diagnostics passed')
