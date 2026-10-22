# Infrastructure-as-Code operations and safety

The Terraform configuration defines an AWS VPC, isolated private subnets, and a default-deny security group.

## Zero-cost workflow

```bash
cd projects/cloud-infrastructure-landing-zone
python3 run.py examples/scenario.json
bash scripts/validate.sh
```

The sample sets `deploy_resources = false` by default. This prevents the module from creating cloud resources, even when someone runs `terraform apply` unintentionally with that default. **Do not turn it on** for this zero-cost portfolio. A paid AWS account is not required for source review or `terraform validate` (provider download needs network access).

Provider download and Terraform state are local. Never commit credentials, state files, or secrets. These Terraform resources have NOT been deployed or validated through AWS runtime tests.

## Engineering boundaries

DNS hostnames disabled, no public IP allocation in subnet settings, private subnet CIDRs. This is a minimal landing-zone skeleton, not a complete enterprise identity/organization baseline, log archive, transit routing, account vending or incident detection service.
