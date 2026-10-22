# Cryptographic Agility, Key Lifecycle and Security Policy Automation

Cryptographic inventory and policy gate for deprecated algorithms and expiring key-material metadata.

**Current implementation:** A reproducible, domain-specific local evaluation engine with a CLI, HTTP endpoint, unit tests and container packaging. This is an independently runnable engineering component, **not** a fully deployed enterprise cryptographic agility, key lifecycle and security policy automation solution.

## Get started

```bash
cd projects/cryptographic-agility-automation
python3 -m unittest discover -s tests -v
python3 run.py examples/scenario.json
python3 server.py
```

To send scenarios over HTTP: `curl -sS -X POST http://127.0.0.1:8080/evaluate -H 'Content-Type: application/json' --data-binary @examples/scenario.json`.

Use `docker compose up --build -d` to start a local container, and `docker compose down` to stop it. **No cloud credentials or paid services are needed.**

## Architecture and project files

- `engine.py` implements cryptographic inventory and policy gate for deprecated algorithms and expiring key-material metadata.
- `run.py` runs the sample scenario.
- `server.py` exposes `GET /healthz` and `POST /evaluate`.
- `examples/scenario.json` provides independently reproducible input data.
- `tests/test_engine.py` contains automated assertions.
- `Dockerfile` and `compose.yaml` create the local deployment.
- `docs/ARCHITECTURE.md` documents scope, trade-offs and known gaps.

**Validation:** Automated tests are provided; CI/runtime validation must still be executed by an independent reviewer. Hosted deployment and production-grade integrations are not claimed.
