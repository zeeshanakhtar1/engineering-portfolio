# Disaster Recovery Drill Runbook

Run `python3 -m unittest discover -s tests -v` and `bash scripts/drill.sh` from this project's directory.

## Backup
`python3 -m dr.backup backup ./data/source ./data/backup.tar.gz`

## Restore
`python3 -m dr.backup restore ./data/backup.tar.gz ./data/restored`

The backup workflow packages regular files (never symlinks), stores per-file SHA-256 digests plus a complete archive hash, verifies both on restore, rejects unsafe archive members, and refuses to overwrite existing restored files. A temporary drill restores and compares the directory contents.

## Scope and limitations
This is local file-level DR, not a real database-transaction-consistent backup. It does not provide geographically independent copies, RPO guarantees, immutable storage, automated scheduling, replication, encryption, key management or cloud disaster recovery. For genuine RPO/RTO evidence, use live workload timestamps and schedule observations independently. No paid cloud resources used.
