#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -v
if command -v kubectl >/dev/null; then kubectl kustomize k8s/overlays/dev >/dev/null; fi
if command -v docker >/dev/null; then docker build -t platform-example-api:local .; fi
