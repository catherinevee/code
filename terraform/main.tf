#==============================
#Cloud Providers
#==============================
provider "aws" {
  region = "us-east-1"
  access_key = var.access_key
  secret_key = var.secret_key
}

provider "azurerm" {
  features {}  
  use_msi = true
}
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
provider "kubernetes" {
  config_path = "kubernetes/kubeconfig.yaml"
  #config_context = ""
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

module "aws_module-apse1" {
  source ="./aws/ap-southeast-1/"
}

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

module "azure_mexicocentral_module" {
  source ="./azure/mexicocentral"
}


#module "azure_westus_module" {
#  source ="./azure/westus/"
#}



