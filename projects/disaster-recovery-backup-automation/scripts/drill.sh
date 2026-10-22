#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
TMP_DIR=$(mktemp -d)
trap 'rm -rf "$TMP_DIR"' EXIT
mkdir -p "$TMP_DIR/source"
printf 'critical-configuration\n' > "$TMP_DIR/source/config.txt"
python3 -m dr.backup backup "$TMP_DIR/source" "$TMP_DIR/backup.tar.gz"
python3 -m dr.backup restore "$TMP_DIR/backup.tar.gz" "$TMP_DIR/restore"
diff -qr "$TMP_DIR/source" "$TMP_DIR/restore"
echo 'Recovery drill: PASS (payload content matched)'
