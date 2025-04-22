terraform {
  #cloud {
  #  organization = "cathyvee-org"
  #  workspaces {
  #    name = "cathyvee"
  #  }
    
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.80.0"
   }
    google = {
      source = "hashicorp/google"
      version = "6.13.0"
    }
    azuredevops = {
      source  = "microsoft/azuredevops"
      version = ">=0.1.0"
    }   
  }

}



# Configure the AWS Provider
provider "aws" {
  access_key = var.AWS_ACCESS_KEY_ID
  secret_key = var.AWS_SECRET_ACCESS_KEY
}


#module "aws_module" {
#  source ="./aws/ap-southeast-1/"
#}

provider "azurerm" {
  features {}  

  use_msi = true
}


#module "azure_paris_module" {
#  source ="./azure/paris"
#}

module "azure_poland_module" {
  source ="./azure/poland/"
}

#module "azure_wetus_module" {
#  source ="./azure/westus/"
#}


provider "google" {
  project     = "development"
  region      = "europe-west4"
}

module "google_module" {
  source = "./gcp/"
}

provider "azuredevops" {
  use_msi = true
}