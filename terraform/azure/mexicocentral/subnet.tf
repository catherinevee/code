resource "azurerm_subnet" "mexicocentralsubnets" {
  name                 = "subnet_${var.defaultlocation}"
  resource_group_name  = azurerm_virtual_network.mexicocentralvnet.resource_group_name
  virtual_network_name = azurerm_virtual_network.mexicocentralvnet.name
  address_prefixes     = ["10.30.1.0/24"]

  }