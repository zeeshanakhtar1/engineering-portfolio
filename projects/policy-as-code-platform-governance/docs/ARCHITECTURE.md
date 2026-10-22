# Architecture — Policy-as-Code, Infrastructure Compliance and Multi-Tenant Security

## Domain scope
Evaluate explicit role-based access rights with a strict cross-tenant denial invariant.

## Execution model
A locally supplied JSON scenario flows through `engine.py`, producing a deterministic structured decision. The CLI and local HTTP adapter invoke the same pure domain function. Docker packages this program without external service dependencies.

## Remaining integration work
The full stated portfolio ambition requires real component integrations, benchmarks under defined conditions, production security controls, automated deployment validation, operational observability, capacity tests and incident/recovery evidence. The implemented workflow is a **locally testable engineering baseline**, not proof of managed cloud or cryptographic interoperability.

## Constraints
No API tokens, paid services, or cloud resources are required. The HTTP example is deliberately unauthenticated and restricted to loopback.
