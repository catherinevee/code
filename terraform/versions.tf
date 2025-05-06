terraform {
  #cloud {
  #  organization = "cathyvee-org"
  #  workspaces {
  #    name = "cathyvee"
  #  }
  required_providers {
    azurerm = {
      source = "hashicorp/azurerm"
      version = ">= 3.107.0, < 4.0"
    }
    aws = {
      source = "hashicorp/aws"
      version = "5.97.0"
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
