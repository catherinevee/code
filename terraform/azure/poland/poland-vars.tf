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
    default = "default_polandresourcegroup"
}


variable "polandcentral-var-prodresourcegroups" {
    type = list(string)
    default = ["polandcentralrg-1",
    "polandcentralrg-2","polandcentralrg-3"]
}

locals {
    defaultsitename = "${var.defaultlocation}-${var.defaultenv}"
    defaultrg = "${var.defaultlocation}-${var.defaultenv}-1"
}

variable "polandcentral-var-prod-allowed-in-tcpports" {
    type = list(string)
    default = ["900","901","9443","443"]
}

variable "polandcentral-var-prod-allowed-in-sourceipv4ranges" {
    type = list(string)
    default = ["10.57.0.0/24","10.70.1.0/24","10.71.2.0/24","10.72.3.0/24"]
}