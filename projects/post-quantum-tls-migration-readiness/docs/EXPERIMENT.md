# Reproducible TLS 1.3 classical vs hybrid key exchange

This experiment performs **actual TLS 1.3 handshakes**, not merely simulated readiness rules.

## Requirements
OpenSSL 3.5 or later with both `X25519` and `X25519MLKEM768` TLS groups available. Confirm:

```bash
openssl version
openssl list -tls-groups
```

## Execute
```bash
cd projects/post-quantum-tls-migration-readiness
python3 -m unittest discover -s tests -v
python3 -m tls_lab.handshake --rounds 10 --output evidence/my-local-run.json
```

The harness generates an ephemeral RSA self-signed certificate with the localhost SAN inside a temporary directory; starts a loopback TLS 1.3 test server; connects with strict verification; measures X25519 and X25519MLKEM768 handshakes; asserts the negotiated group; then terminates the test server and deletes the private key and certificate.

**Important:** This combines hybrid **key exchange** with classical RSA certificate authentication. It does **not** make the certificate's signature post-quantum secure.

## Measurement limitations
Only local process-wall-time measurements. These include OpenSSL command startup and are *not isolated TLS wire-handshake times*. A three-sample exploratory test cannot support statistical conclusions. Larger samples, warmups, confidence intervals, per-stage timestamps and interop across implementations are required.

## Current scope
Real OpenSSL-to-OpenSSL TLS 1.3 group negotiation and cert validation, not multi-vendor interoperability, workload migration, application functionality testing or final research-grade evidence chain.

## Costs and safety
Loopback network only, no cloud accounts or subscriptions. No ephemeral private key is committed to GitHub.
