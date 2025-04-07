resource "azurerm_virtual_network" "poland-vnet-campus" {
    location = azurerm_resource_group.poland-rg-campus.location
    name = "poland-vnet-campus"
    resource_group_name = azurerm_resource_group.poland-rg-campus.name
    address_space = var.address_space
}