#!/usr/bin/env bash
set -euo pipefail
echo "macOS / Apple Silicon engineering environment diagnosis"
for cmd in git python3 docker kind kubectl colima tofu terraform opa openssl gh; do
  if command -v "$cmd" >/dev/null 2>&1; then
    printf 'AVAILABLE %s: %s\n' "$cmd" "$(command -v "$cmd")"
  else
    printf 'OPTIONAL/MISSING %s\n' "$cmd"
  fi
done
echo "No package installation, cloud request, or billable deployment was performed."
