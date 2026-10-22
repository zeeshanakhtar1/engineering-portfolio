# Architecture: Full-Stack Observability, Monitoring and Distributed Tracing

## Implementation
Aggregate latency histograms, request errors and service-level objective violations from synthetic service telemetry.

JSON scenario -> Python evaluation engine -> deterministic JSON result. CLI and locally bound HTTP server call the identical engine implementation. Python standard library only.

## Security and cost
Loopback-only HTTP endpoint, no authentication (therefore **never** expose publicly), non-root container user, read-only container root, no cloud/API clients and no billable cloud services.

## Missing to reach production scope
External systems integration, production network/TLS, realistic persistent workflow orchestration, metrics dashboards, threat modeling, incident and recovery tests, larger benchmarking datasets and platform-specific IaC/deployments require further implementation and verification.

## Reproduce
Run tests, local example, and optional Docker Compose. Independent Kubernetes/managed cloud validation is not claimed.
