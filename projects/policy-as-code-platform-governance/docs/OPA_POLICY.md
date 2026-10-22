# OPA/Rego tenant-access policy

The project includes an actual Rego v1 policy that permits actions only when subjects and resources have equal tenant identifiers and the role includes the requested action.

Run:

```bash
cd projects/policy-as-code-platform-governance
bash scripts/test-policy.sh
```

Three Rego tests cover permitted same-tenant reads, cross-tenant denial and least-privilege denial of unauthorized updates.

OPA is free open-source software. The Rego tests and runtime evaluation have **not yet been executed in the authoring environment**, where the OPA binary was unavailable. The existing Python policy engine and HTTP evaluator provide independent no-package simulations. No cloud account required.
