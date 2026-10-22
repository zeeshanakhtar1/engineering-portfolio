# GPU Workload Scheduling and AI Compute Resource Optimization

Implement priority-ordered and resource-constrained CPU/GPU placement using deterministic bin-packing heuristics.

**Implementation level:** Domain-specific, local-first executable engine with JSON CLI and HTTP API, independently testable sample, and a Docker Compose run target. This is not yet a complete production-grade implementation.

## Run

```bash
cd projects/gpu-ai-workload-scheduling
python3 -m unittest discover -s tests -v
python3 run.py examples/scenario.json
python3 server.py
```

In a second terminal: `curl -sS -X POST http://127.0.0.1:8080/evaluate -H 'Content-Type: application/json' --data-binary @examples/scenario.json`.

Docker alternative: `docker compose up --build -d`, then use the same curl command. Clean up: `docker compose down`.

## Files

- `engine.py`: project-domain decision and validation logic
- `run.py`: CLI scenario execution
- `server.py`: HTTP `/evaluate` and `/healthz`
- `examples/scenario.json`: reproducible scenario
- `tests/test_engine.py`: deterministic assertions
- `Dockerfile`, `compose.yaml`: local packaging/deployment
- `docs/ARCHITECTURE.md`: design constraints, boundaries and remaining work

No cloud credentials or paid accounts are required. **Deployment claims beyond local validation are not made.**
