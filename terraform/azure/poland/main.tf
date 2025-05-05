
module "loadbalancer" {
  source  = "Azure/loadbalancer/azurerm"
  version = "4.4.0"
  resource_group_name = var.defaultrg
}