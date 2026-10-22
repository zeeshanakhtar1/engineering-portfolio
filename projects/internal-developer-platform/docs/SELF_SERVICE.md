# Internal Developer Platform — Local Golden Path

This is a working service scaffolding generator, not a managed IDP control plane.

```bash
cd projects/internal-developer-platform
python3 -m unittest discover -s tests -v
python3 -m idp.scaffold --name billing-api --owner team-platform --output ./generated
cd generated/billing-api
python3 -m app.main
```

The generator creates a functional health-check HTTP application, a non-root Dockerfile, Docker Compose config, ownership metadata and README.

The generator rejects path traversal, invalid names, missing owners and duplicate services. It never provisions cloud infrastructure.

## Missing for a mature IDP

Backstage frontend/catalog, authentication, RBAC, template versioning, policy-as-code admission integration, automated Kubernetes deployment and lifecycle governance are not implemented. Cloud spending remains zero by default.
