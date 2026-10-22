# Local Kubernetes Operations Runbook

## Requirements
Docker daemon, kind, kubectl and Python 3.9+. Intended for local Mac or Linux development only.

## Bootstrap
```bash
cd projects/kubernetes-cluster-operations
bash scripts/check.sh
bash scripts/up.sh
bash scripts/smoke.sh
```

The example API is exposed on localhost port 18080. The cluster has three nodes; the Kubernetes Deployment requests two replicas.

## Diagnose failures
```bash
kubectl get nodes -o wide
kubectl get deployment,pods,svc,pdb,hpa -n engineering-lab
kubectl describe deployment platform-api -n engineering-lab
kubectl get events -n engineering-lab --sort-by=.lastTimestamp
kubectl logs deployment/platform-api -n engineering-lab --tail=50
```

## Recovery experiment (local cluster only)
```bash
kubectl get pods -n engineering-lab -l app=platform-api
kubectl delete pod -n engineering-lab -l app=platform-api --wait=false
kubectl rollout status deployment/platform-api -n engineering-lab --timeout=120s
bash scripts/smoke.sh
```
This intentionally removes matching application pods, so run only in the local lab.

## Teardown
```bash
bash scripts/down.sh
```

## Limitations
HPA requires metrics-server, which is not automatically installed by kind. Prometheus scrape annotations do not install Prometheus. CI is configured but remote GitHub Actions execution is subject to account spending settings. Do not claim production validation.
