variable "defaultrg" {
  type = string
  default = "tfstate"
}

variable "defaultsa" {
  type = string 
  default = "tfstate-sa"
}

variable "defaultsa-container" {
  type = string 
  default = "tfstate-container"  
}


variable "AWS_ACCESS_KEY_ID" {}

variable "AWS_SECRET_ACCESS_KEY" {}

variable "AZURE_CLIENT_ID" {}

variable "AZURE_CLIENT_SECRET" {}

variable "ARM_SUBSCRIPTION_ID" {}

variable "AZURE_TENANT_ID" {}

variable "ARM_ACCESS_KEY" {}


