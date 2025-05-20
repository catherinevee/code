resource "azurerm_virtual_network" "mexicocentralvnet" {
  name                = "vnet_${var.defaultlocation}"
  location            = azurerm_resource_group.polandcentral-prod-resourcegroups[2].location
  resource_group_name = azurerm_resource_group.polandcentral-prod-resourcegroups[2].location
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]

  subnet {
    name             = "1_${azurerm_resource_group.polandcentral-prod-resourcegroups[2].location}_subnet"
    address_prefixes = ["10.0.1.0/24"]
  }

  subnet {
    name             = "2_${azurerm_resource_group.polandcentral-prod-resourcegroups[2].location}_subnet"
    address_prefixes = ["10.0.2.0/24"]
    #security_group   = azurerm_network_security_group.sg.id
  }

  tags = var.tags
}