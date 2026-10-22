# Independent verification and local deployment (Apple Silicon)

## Reference workstation
Apple M5, 24 GB unified memory, 512 GB SSD, macOS. The projects do not require AWS, Azure, GCP or any credit card. Every local container and Kubernetes deployment must be tested on the actual host before it can be considered independently verified.

## Local prerequisites

- Git and Python 3.12+ for Python project test suites
- Docker-compatible container runtime (Colima or Docker Desktop, check license/terms)
- Docker Compose for local service stacks
- kind and kubectl for the Kubernetes platform
- Optional: OpenTofu/Terraform for static IaC validation
- Optional: OpenSSL 3.5+ to run real X25519MLKEM768 TLS 1.3 handshakes
- GitHub CLI (`gh`) for independent repository publication

Install only what is needed for each project. Avoid enabling managed cloud services or submitting payment details just to complete portfolio projects.

## Reproduce and validate

```bash
git clone https://github.com/zeeshanakhtar1/engineering-portfolio.git
cd engineering-portfolio
bash scripts/validate-all.sh
```

Then enter one project directory at a time and follow its own README.

A generic project's command sequence is:

```bash
cd projects/<name>
python3 -m unittest discover -s tests -v
python3 run.py examples/scenario.json
docker compose up --build -d
curl -fsS http://127.0.0.1:8080/healthz
curl -fsS -X POST http://127.0.0.1:8080/evaluate -H 'Content-Type: application/json' --data-binary @examples/scenario.json
docker compose down
```

Do not run all Docker Compose stacks simultaneously: many use host port 8080 and conflict. Some specialized projects use custom commands and ports.

## Project-specific validation

- **Kubernetes:** `bash scripts/check.sh`, `bash scripts/up.sh`, `bash scripts/smoke.sh`, `bash scripts/down.sh` (requires local cluster tools).
- **AIOps:** test and run `python3 -m aiops.api`, then `python3 scripts/smoke.py` from a second terminal.
- **Disaster Recovery:** `bash scripts/drill.sh` executes an actual backup and restore test.
- **MLOps:** `bash scripts/pipeline.sh` generates and evaluates a JSON model artifact from CSV.
- **Post-Quantum TLS:** `python3 -m tls_lab.handshake --rounds 10 --output evidence/my-run.json`; requires supported OpenSSL.
- **Internal Developer Platform:** `python3 -m idp.scaffold --name sample-api --owner team-platform --output ./generated` creates a local starter service.

## Evidence standard

A credible completed project should provide:
1. Exact dependency versions and hardware specifications.
2. Local tests and their command outputs.
3. Reproducible service deployment and teardown.
4. Failure/negative-path tests, not only happy-path outputs.
5. Security and operational limitations.
6. Performance figures with enough samples and measurement methodology.
7. Accurate status labels. A generated program or unit test does not prove a production system works.

## Cost safety

All included cloud deployment functions are off by default. Do not run AWS Terraform apply or deploy managed cloud resources. Use local container runtimes and source validation. GitHub standard hosted runners in public repositories are documented as free; avoid larger runners and chargeable storage/features. Local CPU, electricity and storage usage are not monetary cloud bills but should be monitored.

## Public standalone repositories

Use the opt-in script `scripts/publish-standalone-repositories.sh --dry-run` to preview 26 GitHub repository names. It requires `gh auth login` to your personal GitHub account. The script only publishes on `--execute`; otherwise it cannot mutate your GitHub account. Commit dates remain authentic.
