terraform {
  required_version = ">= 1.4.0"

  required_providers {
    docker = {
      source  = "kreuzwerker/docker"
      version = "4.6.0"
    }
  }
}

provider "docker" {
  host = "npipe:////.//pipe//docker_engine"
}

variable "app_name" {
  type    = string
  default = "student-management-devops"
}

locals {
  container_port = 5000
}

resource "docker_image" "student_app" {
  name = "${var.app_name}:local"

  build {
    context = "${path.module}/../.."
  }

  triggers = {
    app_py       = filesha1("${path.module}/../../app.py")
    dockerfile   = filesha1("${path.module}/../../Dockerfile")
    requirements = filesha1("${path.module}/../../requirements.txt")
  }

  keep_locally = true
}

resource "docker_volume" "student_data" {
  name = "student-data-terraform"
}

resource "docker_container" "student_app" {
  name  = "students-app-terraform"
  image = docker_image.student_app.image_id

  env = [
    "DATABASE_PATH=/app/data/students.db"
  ]

  ports {
    internal = local.container_port
    external = 5001
  }

  volumes {
    container_path = "/app/data"
    volume_name    = docker_volume.student_data.name
  }

  restart = "unless-stopped"
}

output "app_url" {
  value = "http://localhost:5001"
}