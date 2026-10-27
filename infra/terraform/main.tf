terraform {
  required_version = ">= 1.4.0"
}

variable "app_name" {
  type    = string
  default = "student-management-devops"
}

locals {
  container_port = 5000
}

resource "terraform_data" "app_config" {
  input = {
    app_name      = var.app_name
    container_port = local.container_port
  }
}

output "app_name" {
  value = var.app_name
}

output "container_port" {
  value = local.container_port
}