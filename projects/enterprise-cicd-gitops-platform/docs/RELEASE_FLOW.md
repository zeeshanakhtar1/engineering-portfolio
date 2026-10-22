# CI/CD and GitOps delivery flow

1. Developers submit changes through a pull request.
2. Automated source tests, security review and immutable revision verification run.
3. An authorized reviewer approves a release based on the gate engine.
4. A local operator configures Argo CD and reviews the `gitops/application.yaml` Application manifest.
5. Argo CD compares the desired Kubernetes Kustomize overlay with the target local cluster.
6. The operator initiates a sync after reviewing differences, and verifies readiness/rollout.

## Included configuration

`gitops/application.yaml` points to the Kubernetes example in this repository. Automatic sync and destructive pruning are disabled. The local kind deployment uses an image tagged `platform-example-api:local`; without loading the image into the kind nodes, the rollout will not succeed.

## Not yet implemented

An independent ephemeral Argo CD installation, end-to-end GitOps e2e test, artifact signing, SBOM checks and approved rollbacks have not yet been verified. The GitHub Actions workflows do run source tests as configured, subject to the public repository's actions settings.
