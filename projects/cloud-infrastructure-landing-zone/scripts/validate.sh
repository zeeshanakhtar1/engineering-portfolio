#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/../infra/terraform"
if ! command -v terraform >/dev/null 2>&1; then
  echo "Terraform CLI is required for infrastructure syntax validation." >&2
  exit 1
fi
terraform fmt -check -recursive
terraform init -backend=false -input=false
terraform validate -no-color
echo "IaC syntax validated; no infrastructure has been provisioned."
