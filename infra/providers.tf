terraform {
  required_version = ">= 1.6.0"

  backend "s3" {
    # Fill these values using -backend-config or directly here.
    # Example backend config keys:
    # bucket         = "your-terraform-state-bucket"
    # key            = "journal-api/dev/terraform.tfstate"
    # region         = "us-east-1"
    # dynamodb_table = "your-terraform-locks"
    # encrypt        = true
  }

  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = var.aws_region
}
