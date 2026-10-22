output "deployment_enabled" {
  value = var.deploy_resources
}
output "vpc_ids" {
  value = aws_vpc.landing[*].id
}
output "private_subnet_ids" {
  value = { for name, subnet in aws_subnet.private : name => subnet.id }
}
