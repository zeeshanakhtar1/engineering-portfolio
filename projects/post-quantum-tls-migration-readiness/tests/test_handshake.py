import shutil,unittest
from tls_lab.handshake import BASELINE,HYBRID,parse_result,openssl_groups,measure

class HybridTLSTests(unittest.TestCase):
    def test_parser_success(self):
        output='Protocol version: TLSv1.3\nVerification: OK\nVerified peername: localhost\nNegotiated TLS1.3 group: X25519MLKEM768\n'
        parsed=parse_result(output,HYBRID)
        self.assertTrue(all(parsed[key] for key in ('tls13','verified','group_match')))
    def test_parser_group_mismatch(self):
        self.assertFalse(parse_result('Negotiated TLS1.3 group: X25519',HYBRID)['group_match'])
    def test_invalid_rounds(self):
        with self.assertRaises(ValueError):measure(0)
    @unittest.skipUnless(shutil.which('openssl') and HYBRID in openssl_groups(),'OpenSSL with X25519MLKEM768 TLS group unavailable')
    def test_real_local_hybrid_handshakes(self):
        result=measure(1)
        self.assertTrue(result['supported'])
        self.assertTrue(result['results'][BASELINE]['success'])
        self.assertTrue(result['results'][HYBRID]['success'])

if __name__=='__main__':unittest.main()
