# Security auditing and software supply-chain controls

Run `python3 -m security.scan <source-directory>` to check some high-signal secret patterns offline. Findings contain paths, line numbers and rule names, **never the suspected secret value**.

## Additional free security tools (optional)
- `gitleaks detect --source . --redact` for broader secret detection, including Git history.
- `trivy fs --scanners vuln,secret,misconfig .` for filesystem vulnerability and misconfiguration findings.
- `syft dir:. -o spdx-json` for a Software Bill of Materials.

Verify each tool's installation and network/privacy behavior before execution. The source scanner cannot prove security or policy compliance; proper supply-chain security also needs dependency pinning, artifact signing and provenance verification.

## Verification
`python3 -m unittest discover -s tests -v` runs four independent scanner tests.
