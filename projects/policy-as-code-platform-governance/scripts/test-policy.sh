#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
command -v opa >/dev/null || { echo "Install the open-source OPA CLI to test Rego policies"; exit 1; }
opa test policies/ -v
