# AIOps implementation architecture

The pipeline is: Metric producer -> POST /v1/ingest -> SQLite history -> Median Absolute Deviation scoring -> JSON anomaly classification.

### Properties
- Requests are checked for body size, finite numeric values and metric-name length.
- History is read *before* persisting the current sample, avoiding baseline contamination.
- The first five samples are designated warm-up points.
- SQLite and a lock serialize write operations in this single-process HTTP server.
- A persistent Docker named volume survives container restarts.
- Local Docker Compose port publishing binds to loopback, not public interfaces.
- The project uses only standard-library Python for reproducibility.

### Limitations
- This is a local educational baseline, not a production-grade AIOps platform.
- No multivariate ML, event correlation, alerts, encryption, access controls, retention or HA.
- GET /metrics exposes a JSON sample count, not Prometheus text exposition.
- Real deployment to a cloud or managed cluster is intentionally excluded to avoid charges.

### Verification
Run `make test` for eight standard-library tests and `make smoke` with the HTTP server running.
