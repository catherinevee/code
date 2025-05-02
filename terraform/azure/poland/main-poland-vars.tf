#
variable "tfstate_storageaccount" {
    type = string
    default = "tfstatecriy"
}
variable "tfstate_storageaccount_location" {
    type = string
    default = "polandcentralrg-1"
}


#



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

variable "defaultvnet" {
    type = string
    default = "10.0.0.0/16"
}


variable "defaultrg" {
    type = string
    default = "polandcentralrg-dev"
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
