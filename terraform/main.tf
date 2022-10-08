provider "aws" {
  region  = "eu-west-1"
  profile = "development"
}

terraform {
  required_version = ">=1.0.0"
  backend "s3" {
    profile = "development"
    region  = "eu-west-1"
    bucket  = "navenio-global-terraform"
    key     = "infrastructure/testing/helloworld/terraform.tfstate"
    encrypt = true
  }
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = ">=2.51.0"
    }
    sops = {
      source = "carlpett/sops"
      version = ">=0.5.0"
    }
  }
}
