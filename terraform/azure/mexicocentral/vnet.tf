resource "azurerm_virtual_network" "mexicocentralvnet" {
  name                = "vnet_${var.defaultlocation}"
  location            = var.defaultlocation
  resource_group_name = var.mexicocentralresourcegroups[2]
  address_space       = ["10.30.0.0/16"]
  dns_servers         = ["10.30.0.4", "10.30.0.5"]

  tags = var.tags
}