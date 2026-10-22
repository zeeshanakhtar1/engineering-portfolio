# Kubernetes Cluster Operations & Production Workload Management

A locally deployable Kubernetes platform reference implementation, not merely a demo script.

## Implemented components

- Dependency-free Python HTTP service: health/readiness, version endpoint and Prometheus-format metrics.
- Non-root OCI container in `Dockerfile`.
- Declarative three-node kind cluster in `infra/kind/cluster.yaml`.
- Deployment with two replicas, RollingUpdate, readiness/liveness probes, CPU/memory requests and limits, security hardening.
- Kustomize base and development overlay; namespace, NodePort Service, PodDisruptionBudget and HPA.
- Automated bootstrap, local build, smoke checks, verification and teardown in `scripts/`.
- Python HTTP tests in `tests/test_app.py`.
- GitHub Actions workflow at repository root: `.github/workflows/kubernetes-platform-ci.yml`.
- Operational runbook and architecture documentation.

## Requirements

macOS Apple Silicon or Linux with a working Docker-compatible daemon, kind and kubectl. Python 3.9+. No cloud credentials or paid cloud services required. External image pulls require internet access.

## Reproduce locally

```bash
cd projects/kubernetes-cluster-operations
bash scripts/check.sh
bash scripts/up.sh
bash scripts/smoke.sh
curl -fsS http://127.0.0.1:18080/api/v1/info
bash scripts/down.sh
```

## Run tests without Docker or a cluster

```bash
python3 -m unittest discover -s tests -v
```

## Repository layout

- `app/`: HTTP application
- `Dockerfile`: OCI container build
- `infra/kind/`: local cluster provisioner configuration
- `k8s/base/`, `k8s/overlays/dev/`: Kubernetes platform IaC
- `scripts/`: bring-up, smoke test, quality checks and teardown
- `tests/`: API tests
- `docs/`: architecture, limitations and operational runbook

## Verification and limitations

**Verified:** HTTP API tests executed successfully in the build environment. Python compile and shell syntax checks passed locally on a corresponding build.

**Not yet verified:** End-to-end kind cluster bring-up, Docker image execution and the remote GitHub Actions workflow. kind, kubectl and Docker were not available in the build environment. HPA will not function until metrics-server is installed; scrape annotations do not install Prometheus; no Grafana dashboard is currently provided. No production-grade or cloud-deployed claim is made. Remote CI could consume GitHub Actions quotas, so check account spending controls before enabling automated workflows.

This is a substantial platform foundation, but still not a complete enterprise production architecture.
