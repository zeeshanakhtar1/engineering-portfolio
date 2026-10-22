provider "aws" {
  region = var.aws_region
}
resource "aws_vpc" "landing" {
  count                = var.deploy_resources ? 1 : 0
  cidr_block           = var.network_cidr
  enable_dns_support   = true
  enable_dns_hostnames = false
  tags                 = { Name = var.project_name, ManagedBy = "Terraform" }
}
resource "aws_subnet" "private" {
  for_each                = var.deploy_resources ? var.subnets : {}
  vpc_id                  = aws_vpc.landing[0].id
  cidr_block              = each.value.cidr
  availability_zone       = each.value.az
  map_public_ip_on_launch = false
  tags                    = { Name = "${var.project_name}-${each.key}", Tier = "private" }
}
resource "aws_security_group" "deny_ingress" {
  count       = var.deploy_resources ? 1 : 0
  name_prefix = "${var.project_name}-restricted-"
  description = "No ingress and no egress rules by default"
  vpc_id      = aws_vpc.landing[0].id
  ingress     = []
  egress      = []
  tags        = { Name = "${var.project_name}-default-deny" }
}
