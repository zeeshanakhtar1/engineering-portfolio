variable "aws_region" {
  description = "AWS region for provider validation."
  type        = string
  default     = "us-east-1"
}
variable "deploy_resources" {
  description = "Safety interlock: no cloud resources unless deliberately set true."
  type        = bool
  default     = false
}
variable "project_name" {
  type    = string
  default = "engineering-landing-zone"
}
variable "network_cidr" {
  type    = string
  default = "10.42.0.0/16"
  validation {
    condition     = can(cidrhost(var.network_cidr, 0))
    error_message = "network_cidr must be valid."
  }
}
variable "subnets" {
  type = map(object({
    cidr = string
    az   = string
  }))
  default = {
    private_a = { cidr = "10.42.1.0/24", az = "us-east-1a" }
    private_b = { cidr = "10.42.2.0/24", az = "us-east-1b" }
  }
}
