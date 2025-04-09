# Configure the AWS provider
provider "aws" {
  region = "ap-southeast-1"
}

module "s3-bucket" {
  source  = "terraform-aws-modules/s3-bucket/aws"
  version = "4.6.0"
}

module "vpc" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "5.19.0"
}

module "rds" {
  source  = "terraform-aws-modules/rds/aws"
  version = "6.11.0"
  identifier = "demodb"
}