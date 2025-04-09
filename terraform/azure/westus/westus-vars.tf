variable "defaultlocation" {
    type = string
    default = "westus"
}

variable "defaultrg" {
    type = string
    default = "westus-prod1"
}


variable "westus-var-prodresourcegroups" {
    type = list(string)
    default = ["westus-prod1","westus-prod2","westus-prod3"]
}

variable "westus-var-devresourcegroups" {
    type = list(string)
    default = ["westus-dev1","westus-dev2","westus-dev3"]
}

variable "westus-var-prod-allowed-in-tcpports" {
    type = list(string)
    default = ["900","901","9443","443"]
}

variable "westus-var-prod-allowed-in-sourceipv4ranges" {
    type = list(string)
    default = ["10.57.0.0/24","10.70.1.0/24","10.71.2.0/24","10.72.3.0/24"]
}