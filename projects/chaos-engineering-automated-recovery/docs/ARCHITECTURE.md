# Architecture — Chaos Engineering and Automated Service Recovery

## Scope
Non-mutating chaos fault admission controller with availability budget enforcement; no faults applied automatically.

## Request path
Local JSON input -> validated domain evaluation in `engine.py` -> deterministic JSON decision/report. The same engine is accessible through the CLI and a loopback-only HTTP server.

## Security and cost
The HTTP endpoint is loopback-bound, intentionally unauthenticated, and suitable **only** for local development. The container runs as an unprivileged UID, has a read-only root filesystem, and binds to localhost. No calls are made to commercial cloud services, and no credentials are needed.

## Non-goals / outstanding work
Deployment to a managed provider, true multi-node orchestration, full IaC environments, enterprise authentication, synthetic load measurement, monitoring dashboards, and operational recovery are outside this baseline. Do not represent this as verified production readiness.

## Verification
Run `make test`, `make run`, and `docker compose up --build -d` followed by the documented `curl` request. Docker requires a local compatible engine.
