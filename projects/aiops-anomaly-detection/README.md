# AIOps Anomaly Detection & Infrastructure Event Intelligence

A runnable local-first telemetry ingest service with SQLite storage and robust median absolute deviation anomaly scoring.

**Status:** Functional local baseline; production features and event correlation not yet implemented. No cloud services are required.

## Quick start
```bash
cd projects/aiops-anomaly-detection
python3 -m unittest discover -s tests -v
python3 -m aiops.api
```

From another terminal:
```bash
python3 scripts/smoke.py
```

Or use Docker Compose: `docker compose up --build -d`, then run the smoke test; clean up with `docker compose down`.

## Architecture
`metric producer -> POST /v1/ingest -> SQLite history -> MAD detector -> JSON response`

The first five samples warm the history. The response includes a baseline, robust score, anomaly Boolean and reason. The ingestion handler validates request size, metric name and numeric finiteness.

## Project files
- `aiops/core.py`: robust outlier detection implementation.
- `aiops/store.py`: SQLite schema and persistence.
- `aiops/api.py`: HTTP ingestion, health and sample-count endpoint.
- `tests/test_aiops.py`: eight independent tests including HTTP integration.
- `scripts/smoke.py`: end-to-end smoke test.
- `Dockerfile`, `compose.yaml`: reproducible local container execution.
- `Makefile`: build/test/run commands.
- `docs/ARCHITECTURE.md`: design decisions, limitations and verification.

## HTTP API
- `GET /healthz` gives service health.
- `GET /metrics` gives JSON sample count (not Prometheus format).
- `POST /v1/ingest` accepts `{"metric":"cpu","value":85.0}` and returns classification.

Do not expose this unauthenticated local example on public networks. Multi-source correlation and alert pipelines remain future milestones.
