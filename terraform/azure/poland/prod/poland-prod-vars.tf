variable "poland-var-prodresourcegroups" {
    type = list(string)
    default = ["poland-prod1","poland-prod2","poland-prod3"]
}

variable "poland-var-prod-allowed-in-tcpports" {
    type = list(string)
    default = ["900","6515","9443","443"]
}

variable "poland-var-prod-allowed-in-sourceipv4ranges" {
    type = list(string)
    default = ["10.101.0.0/24","10.101.1.0/24","10.101.2.0/24","10.101.3.0/24"]
}