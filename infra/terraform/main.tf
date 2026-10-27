terraform {
  required_version = ">= 1.0"
}

variable "app_name" {
  type    = string
  default = "student-management-devops"
}

locals {
  container_port = 5000
}

output "app_name" {
  value = var.app_name
}

output "container_port" {
  value = local.container_port
}