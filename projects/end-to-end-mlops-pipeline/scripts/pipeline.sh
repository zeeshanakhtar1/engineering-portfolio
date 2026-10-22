#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
python3 -m unittest discover -s tests -v
python3 -m mlops.train --data datasets/training.csv --output artifacts/model.json
python3 -m mlops.predict --model artifacts/model.json --feature 12
