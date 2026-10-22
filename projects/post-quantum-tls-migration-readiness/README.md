# Post-Quantum Cryptography Migration Readiness and Hybrid TLS Validation

Assess an evidence-based hybrid TLS 1.3 migration decision from supplied validation results. Does NOT perform a real X25519+ML-KEM handshake.

## What is implemented

A project-specific deterministic evaluation engine, CLI, HTTP interface, Dockerfile/Compose local deployment, recorded example scenario and automated contract tests. These components are real source code, but this project is **not yet** a complete production implementation of its broader scope.

## Reproduce

```bash
cd projects/post-quantum-tls-migration-readiness
python3 -m unittest discover -s tests -v
python3 run.py examples/scenario.json
python3 server.py
```

In a second terminal:

```bash
curl -fsS -X POST http://127.0.0.1:8080/evaluate -H 'Content-Type: application/json' --data-binary @examples/scenario.json
```

For container deployment, run `docker compose up --build -d` and use the same HTTP command, then `docker compose down`.

## Source files

`engine.py` (domain logic), `run.py` (CLI), `server.py` (HTTP), `tests/test_engine.py` (tests), `examples/scenario.json` (fixtures), `Dockerfile`, `compose.yaml`, `Makefile`, and `docs/ARCHITECTURE.md`.

**Costs:** No cloud deployment occurs; services only bind to localhost. Do not expose the unauthenticated HTTP service publicly.
