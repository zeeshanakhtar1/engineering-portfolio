# Decision controller architecture

`Metric source -> input validation -> policy thresholds -> cooldown/bounds -> decision -> JSONL audit`

The controller deliberately never mutates real infrastructure. Decisions include `execute: false`. A safe bounded change is proposed but is not applied to Kubernetes or cloud systems.

Controls include replica limits, single-step updates, a cooldown, strict threshold separation, and append-only audit events.

**Future work:** telemetry ingestion, full reconciliation, policy approvals, simulated actuator, Kubernetes dry-run adapter, failure replay and leader election.
