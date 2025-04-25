

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
    default = "polandcentralrg-2"
}

variable "defaultsa" {
    type = string
    default = "polandsa"
}


variable "polandcentral-var-prodresourcegroups" {
    type = list(string)
    default = ["polandcentralrg-prod",
    "polandcentralrg-test","polandcentralrg-dev"]
}
