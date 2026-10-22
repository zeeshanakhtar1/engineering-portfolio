# Networking fault isolation

Probe a locally running HTTP application in the repository using:

```bash
python3 -m unittest discover -s tests -v
python3 -m netdiag.probe 127.0.0.1 --port 8091
```

AIOps uses port 8091, Kubernetes example uses port 18080. Probe results show DNS resolution, TCP connectivity and HTTP status. HTTPS probes additionally validate an actual TLS handshake and certificate using Python's default trust store.

**Production caution:** An HTTP health check returning 200 is not proof of end-to-end service functionality. Error details can include hostnames and should be handled as internal diagnostics.

The staged probe is a real network diagnostic, but it does not replace packet capture, traceroute, tcpdump, DNS debugging, kernel tracing or a production network observability stack. No paid resources are required.
