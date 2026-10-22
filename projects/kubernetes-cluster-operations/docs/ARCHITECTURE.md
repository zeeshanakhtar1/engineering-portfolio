# Kubernetes Operations Architecture

Local-only workload deployment with a 2-replica unprivileged nginx example, resource limits, probes, and a ClusterIP service.

## Run (requires a local Kubernetes cluster and kubectl)

```bash
kubectl apply -f manifests/deployment.yaml
kubectl apply -f manifests/service.yaml
kubectl rollout status deployment/example-api --timeout=120s
kubectl get pods -l app=example-api
kubectl port-forward service/example-api 8080:80
```

In another terminal: `curl http://127.0.0.1:8080`.

## Limits

These manifests are a local Kubernetes demonstration, not a fully validated production deployment. They have not been executed against a cluster in this publishing session. Image downloads require network access. No cloud account is required.

## Cleanup

```bash
kubectl delete -f manifests/service.yaml -f manifests/deployment.yaml
```
