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
provider "azurerm" {
  features {}  
  use_msi = true
}
provider "google" {
  project     = "development"
  region      = "europe-west4"
}
provider "local" {
}
provider "kubernetes" {
  config_path = "kubernetes/kubeconfig.yaml"
  #config_context = ""
}


module "google_module" {
  source = "./gcp/"
}

provider "azuredevops" {
  use_msi = true
}

module "azure_poland_module" {
  source ="./azure/poland/"
}




#module "aws_module" {
#  source ="./aws/ap-southeast-1/"
#}

#module "azure_paris_module" {
#  source ="./azure/paris"
#}



#module "azure_westus_module" {
#  source ="./azure/westus/"
#}



