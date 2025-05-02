

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
    default = "poland_analytics_workspace"
}

variable "defaultcontainerappenv" {
    type = string
    default = "containerappenv_default"
}

variable "defaultcontainerapp" {
    type = string
    default = "containerapp_default"
}

variable "polandcentral-var-prodresourcegroups" {
    type = list(string)
    default = [
         "polandcentralrg-prod",
         "polandcentralrg-test",
         "polandcentralrg-dev"
        ]
}
