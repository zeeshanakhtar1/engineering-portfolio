# Local metrics observability deployment

This is a **real local Prometheus/Grafana stack**, not a claim that Loki, Tempo or end-to-end OpenTelemetry distributed tracing have been implemented.

## Prerequisites

Run the local Kubernetes Cluster Operations project, which exposes an application metrics endpoint at `localhost:18080/metrics`. It must return Prometheus text exposition.

## Bring up

```bash
cd projects/full-stack-observability-platform/observability
cp .env.example .env
# Edit .env and supply a strong unique local password.
docker compose up -d
```

Grafana: http://localhost:3000; Prometheus: http://localhost:9090.

In Grafana query `http_requests_total`. If Prometheus reports targets DOWN, verify the Kubernetes project and `host.docker.internal` routing (runtime-specific).

`docker compose down` stops services. `docker compose down -v` also deletes persisted Grafana data.

## Security and costs

Only loopback port bindings. No cloud service accounts. The repository does not contain a real password: the example is a placeholder and must be changed in `.env`.

## Gaps

No verified multi-service log aggregation, Tempo tracing backend, on-call paging or burn-rate alert rules. Images have not been pulled and launched in this session; operator validation required.
