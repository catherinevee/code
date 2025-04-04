variable "dev_environment_type" {
    type = list(string)
    default = ["cathy-dev1","cathy-test2","cathy-dev3"]
}
#var.environment_type[count.index]
#for_each = toset(var.environment_type)
#name = each.value

#vnet_vpc_type = "${var.environment == "prod" ? "10.111.0.0/24" : "10.100.0.0/24"}"

variable "allowed_nsg_ports" {
  type = list(string)
  default = ["522","900","443"]
}