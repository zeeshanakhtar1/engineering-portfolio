# Bounded local HTTP load tests

Run unit tests: `python3 -m unittest discover -s tests -v`

Start any repository example service with a `/healthz` endpoint, e.g. AIOps, and then benchmark it:

```bash
python3 -m loadtest.runner --url http://127.0.0.1:8091/healthz --requests 100 --concurrency 4
```

The runner records a real request duration for each response and reports throughput, duration, error ratio, and nearest-rank p50/p95/p99 latency. Run under repeated conditions and keep system load constant before comparing benchmarks.

**Safety:** Only localhost targets are permitted, with at most 1000 total requests and 16 concurrent workers. This avoids inadvertently stressing third-party services. No cloud services are used.

**Limitations:** This is not a full distributed load testing system, open-loop arrival model, coordinated-omission correction, or large-scale capacity test. For heavier studies, add a separate reviewed experiment with k6 or Locust and explicit target authorization.
