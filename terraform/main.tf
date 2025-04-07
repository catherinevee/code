terraform {
  cloud {
    organization = "cathyvee-org"
    workspaces {
      name = "cathyvee"
    }
  }  
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = "4.11.0"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.80.0"
   }
    google = {
      source = "hashicorp/google"
      version = "6.13.0"
    }   
  }
}

# Configure the AWS Provider
provider "aws" {
  region     = "us-west-1"
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}


module "aws_module" {
  source ="./aws"
}

provider "azurerm" {
  features {}  
  client_id = var.AZURE_CLIENT_ID
  client_secret = var.AZURE_CLIENT_SECRET
  subscription_id = var.ARM_SUBSCRIPTION_ID
  tenant_id = var.AZURE_TENANT_ID
  
}


#module "azure_paris_module" {
#  source ="./azure/paris"
#}

module "azure_poland_module" {
  source ="./azure/poland/dev"
}

provider "google" {
  project     = "development"
  region      = "europe-west4"
}

module "google_module" {
  source = "./gcp/"
}