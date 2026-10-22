# Engineering Portfolio — Real Systems, Reproducible Evidence

A continuously developed engineering portfolio spanning cloud infrastructure, reliability, systems architecture, DevOps, platform engineering, machine learning infrastructure, AIOps, security and engineering research.

**Source-code status (October 2026):** All 26 project directories have project-specific executable components, automated test contracts, local packaging and documented limitations. **They are not 26 completed enterprise production systems.** Some are working operational components; others are domain simulators pending integrations.

## Explore the engineering projects

### Cloud Infrastructure, DevOps & Systems Engineering

| Project | Current implemented component |
|---|---|
| [Production-Ready Cloud Infrastructure & Landing Zone](projects/cloud-infrastructure-landing-zone/README.md) | Network checks, guarded AWS VPC Terraform skeleton |
| [Kubernetes Cluster Operations & Production Workload Management](projects/kubernetes-cluster-operations/README.md) | Three-node kind config, Kustomize workload, CI and runbooks |
| [Enterprise CI/CD Automation & GitOps Delivery Platform](projects/enterprise-cicd-gitops-platform/README.md) | Release gate simulator and Argo CD Application |
| [Full-Stack Observability, Monitoring & Distributed Tracing](projects/full-stack-observability-platform/README.md) | SLO evaluator and local Prometheus/Grafana stack (tracing pending) |
| [Linux Systems, Network Diagnostics & Failure Engineering](projects/linux-network-failure-engineering/README.md) | Staged DNS/TCP/TLS/HTTP probes and tests |

### Site Reliability, Security & Resilience

| Project | Current implemented component |
|---|---|
| [Chaos Engineering & Automated Service Recovery](projects/chaos-engineering-automated-recovery/README.md) | Disruption policy gate (fault execution pending) |
| [Disaster Recovery, Backup Automation & Business Continuity](projects/disaster-recovery-backup-automation/README.md) | Actual backup/restore CLI, SHA-256 integrity and verified recovery drill |
| [Cloud Infrastructure Cost Optimization & Kubernetes FinOps](projects/cloud-cost-optimization-finops/README.md) | Offline savings model and zero-cost budget gate |
| [DevSecOps Automation & Software Supply Chain Security](projects/devsecops-supply-chain-security/README.md) | Artifact policy gates plus offline credential-pattern scanner |
| [Distributed Application Performance, Load & Capacity Engineering](projects/performance-load-capacity-engineering/README.md) | Bounded localhost HTTP load generator plus p50/p95/p99 metrics |

### Platform Engineering & Enterprise Architecture

| Project | Current implemented component |
|---|---|
| [Internal Developer Platform & Self-Service Infrastructure Provisioning](projects/internal-developer-platform/README.md) | Resource admission gate plus local service scaffolding generator |
| [Engineering Service Catalog & Software Architecture Governance](projects/engineering-service-catalog/README.md) | Service ownership/dependency validator |
| [Policy-as-Code, Infrastructure Compliance & Multi-Tenant Security](projects/policy-as-code-platform-governance/README.md) | Tenant-scoped RBAC evaluation |
| [Multi-Cloud Infrastructure Architecture & Deployment Orchestration](projects/multi-cloud-infrastructure-orchestration/README.md) | Provider placement evaluator; cloud deployments disabled |

### Machine Learning Infrastructure & MLOps

| Project | Current implemented component |
|---|---|
| [End-to-End Machine Learning Pipeline & MLOps Automation](projects/end-to-end-mlops-pipeline/README.md) | Deterministic CSV OLS training, SHA-256 model artifact and inference |
| [Production Machine Learning Model Serving & Inference Monitoring](projects/ml-model-serving-inference-monitoring/README.md) | Prediction/SLO evaluator |
| [GPU Workload Scheduling & AI Compute Resource Optimization](projects/gpu-ai-workload-scheduling/README.md) | Priority-based CPU/GPU placement simulator |
| [Machine Learning Observability, Data Drift & Model Performance Monitoring](projects/ml-observability-drift-detection/README.md) | Feature distribution drift evaluator |

### AIOps & Autonomous Infrastructure

| Project | Current implemented component |
|---|---|
| [AIOps Anomaly Detection & Infrastructure Event Intelligence](projects/aiops-anomaly-detection/README.md) | HTTP ingestion, SQLite and MAD anomaly detection |
| [Intelligent Incident Diagnosis & Automated Infrastructure Remediation](projects/intelligent-incident-remediation/README.md) | Safe diagnosis recommendations (no execution) |
| [Infrastructure Digital Twin & Predictive Failure Simulation](projects/infrastructure-digital-twin/README.md) | Dependency failure propagation simulator |
| [Autonomous Infrastructure Control & Closed-Loop Self-Healing Systems](projects/autonomous-infrastructure-controller/README.md) | Policy-bounded scaling decisions with audit trail (no execution) |

### Advanced Security, Distributed Computing & Research

| Project | Current implemented component |
|---|---|
| [Post-Quantum Cryptography Migration Readiness & Hybrid TLS Validation](projects/post-quantum-tls-migration-readiness/README.md) | Evidence classifier plus real local X25519/X25519MLKEM768 TLS 1.3 handshake harness |
| [Cryptographic Agility, Key Lifecycle & Security Policy Automation](projects/cryptographic-agility-automation/README.md) | Algorithm/key policy inventory |
| [Heterogeneous Computing & Adaptive Workload Orchestration](projects/heterogeneous-compute-orchestrator/README.md) | CPU/GPU scheduling under cost/latency constraints |
| [Cross-System Reliability Intelligence & Distributed Infrastructure Analytics](projects/cross-system-reliability-intelligence/README.md) | Transitive blast-radius analysis |

## Independent verification

The main projects are organized into `projects/<descriptive-project-name>/`.

```bash
git clone https://github.com/zeeshanakhtar1/engineering-portfolio.git
cd engineering-portfolio
bash scripts/validate-all.sh
```

To execute an individual project, open its README and follow the commands. For most projects:

```bash
cd projects/<descriptive-project-name>
python3 -m unittest discover -s tests -v
python3 run.py examples/scenario.json
# Optional, only with a Docker-compatible runtime:
docker compose up --build -d
```

**Exceptions:** Kubernetes, AIOps, autonomous controller and backup/recovery have additional project-specific commands and multi-file implementations. Follow their own READMEs.

## Engineering validation and evidence

- AIOps API: eight local unit/integration tests and HTTP anomaly ingestion smoke test passed during implementation.
- Autonomous Infrastructure Controller: eight unit tests and a local CLI decision demonstration passed.
- Disaster Recovery: four file-backup tests and a local restore/integrity drill passed.
- DevSecOps, Performance Engineering, Internal Developer Platform and MLOps training: four additional tests in each project passed locally.
- Linux Network Diagnostics: three live networking probe tests passed locally.
- Post-Quantum TLS: four tests passed, including a **real** OpenSSL 3.5.5 hybrid TLS 1.3 handshake integration test; preliminary measurements are in the project's `evidence/` directory.
- Kubernetes platform: HTTP application tests were executed; full Docker/kind cluster deployment has **not** been independently verified.
- Remaining project engines: tests are committed and a GitHub Actions validation workflow exists, but a completed CI run has **not** been verified in this session.
- Terraform, Argo CD, Prometheus/Grafana, managed environments and GPU runtimes have **not** been validated end to end. The PQC project has verified local OpenSSL-to-OpenSSL handshakes, but not cross-vendor interoperability.

## Zero-cost engineering policy

Everything defaults to local simulation or static validation, with no billable cloud deployment. The AWS Terraform module's `deploy_resources` is `false` by default; do not override it for this portfolio. Docker and standard local open-source tools need no cloud subscription. Check local storage and resource availability, and do not assume all optional Docker images are preinstalled.

Our public GitHub workflow uses a standard GitHub-hosted runner; GitHub documents standard runners in public repositories as free, but larger runners and some storage/features can be charged. No paid runners, managed cloud clusters or paid CI services are required.

## Integrity

No fabricated historical commit dates, results, customer data or production claims. Project README files describe exactly what is implemented and what remains. This repository demonstrates progressively developed engineering components and is not a guarantee of production readiness.

[See open project implementation issues](https://github.com/zeeshanakhtar1/engineering-portfolio/issues) · [Portfolio planning board](https://github.com/users/zeeshanakhtar1/projects/1)

## Standalone GitHub repositories

This is currently **one monorepo containing 26 individually runnable project directories**, not 26 separate live repositories. To create 26 standalone public repositories under the authenticated personal account, review and run `scripts/publish-standalone-repositories.sh --dry-run` first, then explicitly opt into `--execute`. The script does not backdate commits, uses no paid cloud services, and never overwrites existing repositories. It requires local GitHub CLI authentication and is not executed automatically.
