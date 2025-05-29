#==============================
#Cloud Provider Configuration
#==============================

#call like:
#resource "azurerm_resource_group" "rg2" {
#  provider = azurerm.catherineprod
#}

#use input variables during the pipeline 
#to change between subscriptions

#production subscriptions
#aws

provider "aws" {
  access_key = var.access_key
  secret_key = var.secret_key
} 


provider "aws" {
  alias = "catherineprod"
  access_key = var.access_key
  secret_key = var.secret_key
} 
provider "aws" {
  alias = "catherinedev"
  access_key = var.access_key
  secret_key = var.secret_key
}
provider "aws" {
  alias = "catherinetest"
  access_key = var.access_key
  secret_key = var.secret_key
}

#azure
provider "azurerm" {
  features {}  
  use_msi = true
}

provider "azurerm" {
  alias = "catherineprod"
  features {}  
  use_msi = true
}
provider "azurerm" {
  alias = "catherinedev"
  features {}  
  use_msi = true
}
provider "azurerm" {
  alias = "catherinetest"
  features {}  
  use_msi = true
}

#gcp
provider "google" {
  project     = "development"
  region      = "europe-west4"
}

#==============================
#Dedicated Providers
#==============================

provider "local" {}
provider "azuredevops" {
  use_msi = true
}

#provider "kubernetes" {
#  config_path = "kubernetes/kubeconfig.yaml"
  #config_context = ""
#}


provider "spotinst" {
   token   = "${var.spotinst_token}"
   account = "${var.spotinst_account}"
}

#==============================
#Child Modules
#==============================

#==============================
#GCP
module "google_module" {
  source = "./gcp/"
}


#==============================
#AWS

#module "aws_module-apne1" {
#  source ="./aws/ap-northeast-1/"
#}

#module "aws_module-apse1" {
#  source ="./aws/ap-southeast-1/"
#}

#module "ca-central-1" {
#  source = "./aws/ca-central-1/"
#}

#module "aws_module-use1" {
#  source ="./aws/us-east-1/"
#}

#module "aws_module-usw1" {
#  source ="./aws/us-west-1/"
#}
#==============================
#Azure

#module "azure_poland_module" {
#  source ="./azure/poland/"
#}

#module "azure_francecentral_module" {
#  source ="./azure/francecentral"
#}

#module "azure_mexicocentral_module" {
#  source ="./azure/mexicocentral"
#}


#module "azure_westus_module" {
#  source ="./azure/westus/"
#}



