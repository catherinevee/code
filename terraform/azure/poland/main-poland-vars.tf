#
variable "tfstate_storageaccount" {
    type = string
    default = "tfstatecriy"
}
variable "tfstate_storageaccount_rg" {
    type = string
    default = "tfstate-rg"
}



variable "tags" {
  description = "Common tags for all resources"
  type = object({
    Environment = string
    OU   = string
  })
  default = {
    Environment = "prod"
    OU   = "IT"
  }
}




variable "defaultemail" {
    type = string
    default = "catherine.vee@outlook.com"
}

variable "defaultname" {
    type = string
    default = "Catherine Vee"
}

variable "defaultlocation" {
    type = string
    default = "polandcentral"
}
variable "defaultenv" {
  type = string
  default = "prod"
}

variable "defaultaks_clustername" {
    type = string
    default = "cathy-prod-cluster"
}


variable "defaultaks_dnsname" {
    type = string
    default = "catherine89102nf"
}

variable "defaultvnet" {
    type = string
    default = "10.0.0.0/16"
}


variable "defaultrg" {
    type = string
    default = "polandcentralrg-prod"
}

variable "defaultsa" {
    type = string
    default = "polandsa"
}

variable "defaultanalyticsworkspace" {
    type = string
    default = "poland-analytics-workspace"
}

variable "defaultcontainerappenv" {
    type = string
    default = "containerappenv-default"
}

variable "defaultcontainerapp" {
    type = string
    default = "containerapp-default"
}

variable "polandcentral-var-prodresourcegroups" {
    type = list(string)
    default = [
         "polandcentralrg-prod",
         "polandcentralrg-test",
         "polandcentralrg-dev"
        ]
}
