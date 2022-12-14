provider "aws" {
  region  = "eu-west-1"
  profile = "development"
}

terraform {
  required_version = ">=1.0.0"
  backend "s3" {
    profile = "development"
    region  = "eu-west-1"
    bucket  = "kostas-terraform-playground"
    key     = "infrastructure/project/hello-world/terraform.tfstate"
    encrypt = true
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=2.51.0"
    }
  }
}
