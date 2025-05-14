# Configure the AWS Provider
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

#module "azure_poland_module" {
#  source ="./azure/poland/"
}



module "aws_module-apse1" {
  source ="./aws/ap-southeast-1/"
}


module "aws_module-use1" {
  source ="./aws/us-east-1/"
}

module "aws_module-usw1" {
  source ="./aws/us-west-1/"
}

#module "azure_paris_module" {
#  source ="./azure/paris"
#}



#module "azure_westus_module" {
#  source ="./azure/westus/"
#}



