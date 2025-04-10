variable "defaultlocation" {
    type = string
    default = "polandcentral"
}
variable "defaultenv" {
  type = string
  default = "prod"
}

variable "defaultrg" {
    type = string
    default = "${var.defaultlocation}-${var.defaultenv}-1"
}


variable "polandcentral-var-prodresourcegroups" {
    type = list(string)
    default = ["${var.defaultlocation}-${var.defaultenv}-1",
    "${var.defaultlocation}-${var.defaultenv}-2","${var.defaultlocation}-${var.defaultenv}-3"]
}

variable "polandcentral-var-prod-allowed-in-tcpports" {
    type = list(string)
    default = ["900","901","9443","443"]
}

variable "polandcentral-var-prod-allowed-in-sourceipv4ranges" {
    type = list(string)
    default = ["10.57.0.0/24","10.70.1.0/24","10.71.2.0/24","10.72.3.0/24"]
}