# ML Model Serving Inference Monitoring

## Current implementation

Compute inference results and service-level compliance.

**Status:** Small, dependency-free local proof of concept. Not a complete production system. It does not deploy cloud infrastructure or incur cloud charges.

## Files

- [demo.py](demo.py) — runnable implementation and built-in assertions
- [tests/test_demo.py](tests/test_demo.py) — independent unittest-based checks
- [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md) — architecture, scope and limitations

## Run locally

From the root of the engineering-portfolio repository:

```bash
python3 projects/ml-model-serving-inference-monitoring/demo.py
python3 -m unittest discover -s projects/ml-model-serving-inference-monitoring/tests -p 'test_*.py'
```

Python 3.9+ recommended; no external packages, credentials, subscriptions or cloud accounts required.

## Development roadmap

- [ ] Implement substantive, project-specific infrastructure and application workflows
- [ ] Add realistic local integration scenarios and negative-path tests
- [ ] Capture reproducible performance, failure, and security evidence
- [ ] Review architecture trade-offs and operational runbooks
- [ ] Validate the finished solution on the intended runtime

See the GitHub Issues board for tracking. Do not interpret this README as a production-readiness claim.
