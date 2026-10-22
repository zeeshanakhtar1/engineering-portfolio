#!/usr/bin/env bash
# Opt-in creation of 26 standalone public repos; no cloud deployment or backdating.
set -euo pipefail
MODE=${1:---dry-run}
[[ "$MODE" == "--dry-run" || "$MODE" == "--execute" ]] || { echo "Use --dry-run or --execute"; exit 2; }
ROOT=$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)
OWNER=zeeshanakhtar1
command -v gh >/dev/null || { echo "Install GitHub CLI"; exit 1; }
command -v git >/dev/null || { echo "Install Git"; exit 1; }
LOGIN=$(gh api user --jq .login)
[[ "$LOGIN" == "$OWNER" ]] || { echo "Authenticated as $LOGIN, not $OWNER; refusing"; exit 1; }
if [[ "$MODE" == "--execute" ]]; then
  git config user.name >/dev/null || { echo "Set git user.name"; exit 1; }
  git config user.email >/dev/null || { echo "Set git user.email"; exit 1; }
fi
shopt -s nullglob
projects=("$ROOT"/projects/*)
[[ "${#projects[@]}" -eq 26 ]] || { echo "Expected exactly 26 project folders"; exit 1; }
for source in "${projects[@]}"; do
  name=$(basename "$source")
  [[ "$name" =~ ^[a-z][a-z0-9-]+$ ]] || { echo "Invalid repo name: $name"; exit 1; }
  if gh repo view "$OWNER/$name" >/dev/null 2>&1; then
    echo "EXISTS https://github.com/$OWNER/$name"
    [[ "$MODE" == "--dry-run" ]] || { echo "Refusing to overwrite existing repo"; exit 1; }
    continue
  fi
  echo "NEW https://github.com/$OWNER/$name"
  [[ "$MODE" == "--execute" ]] || continue
  tmp=$(mktemp -d)
  cp -R "$source"/. "$tmp"/
  mkdir -p "$tmp/.github/workflows"
  cat > "$tmp/.github/workflows/unit-tests.yml" <<'YAML'
name: Unit Tests
on: [push, pull_request, workflow_dispatch]
permissions:
  contents: read
jobs:
  test:
    runs-on: ubuntu-latest
    timeout-minutes: 10
    steps:
      - uses: actions/checkout@v4
      - uses: actions/setup-python@v5
        with:
          python-version: '3.12'
      - run: python -m unittest discover -s tests -v
YAML
  git -C "$tmp" init -b main -q
  git -C "$tmp" add -A
  git -C "$tmp" commit -qm "Initial standalone publication: $name"
  (cd "$tmp" && gh repo create "$OWNER/$name" --public --source . --remote origin --push)
  rm -rf "$tmp"
  echo "PUBLISHED https://github.com/$OWNER/$name"
done
