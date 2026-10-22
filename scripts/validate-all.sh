#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
count=0
failed=0
for project in projects/*; do
  if [ -d "$project/tests" ]; then
    echo "TEST PROJECT: $project"
    if (cd "$project" && python3 -m unittest discover -s tests -p 'test_*.py' -v); then
      count=$((count+1))
    else
      failed=$((failed+1))
    fi
  else
    echo "MISSING TEST SUITE: $project" >&2
    failed=$((failed+1))
  fi
done
echo "Test suites passed: $count / 26; failed or missing: $failed"
[ "$count" -eq 26 ] && [ "$failed" -eq 0 ]
