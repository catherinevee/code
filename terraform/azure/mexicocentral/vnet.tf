resource "azurerm_virtual_network" "mexicocentralvnet" {
  name                = "vnet_${var.defaultlocation}"
  location            = azurerm_resource_group.polandcentral-prod-resourcegroups[2].location
  resource_group_name = azurerm_resource_group.polandcentral-prod-resourcegroups[2].location
  address_space       = ["10.0.0.0/16"]
  dns_servers         = ["10.0.0.4", "10.0.0.5"]

  tags = var.tags
}