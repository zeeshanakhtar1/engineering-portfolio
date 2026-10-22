#!/usr/bin/env bash
set -euo pipefail
for path in healthz readyz api/v1/info metrics; do
  curl --fail --silent --show-error --max-time 5 "http://127.0.0.1:18080/$path" >/dev/null
done
kubectl rollout status deployment/platform-api -n engineering-lab --timeout=30s
kubectl get pods -n engineering-lab -l app=platform-api
echo "HTTP and workload smoke checks passed"
