#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
for cmd in docker kind kubectl; do command -v "$cmd" >/dev/null || { echo "Missing required tool: $cmd" >&2; exit 1; }; done
kind get clusters | grep -qx engineering-platform || kind create cluster --config infra/kind/cluster.yaml
docker build -t platform-example-api:local .
kind load docker-image platform-example-api:local --name engineering-platform
kubectl apply -k k8s/overlays/dev
kubectl rollout status deployment/platform-api -n engineering-lab --timeout=180s
echo "Application URL: http://localhost:18080/api/v1/info"
