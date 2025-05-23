resource "azurerm_subnet" "mexicocentralsubnet_prod" {
  name                 = "subnet-prod_${var.defaultlocation}"
  resource_group_name  = azurerm_virtual_network.mexicocentralvnet.resource_group_name
  virtual_network_name = azurerm_virtual_network.mexicocentralvnet.name
  address_prefixes     = ["10.30.1.0/24"]
  }

resource "azurerm_subnet" "mexicocentralsubnet_dev" {
  name                 = "subnet-dev_${var.defaultlocation}"
  resource_group_name  = azurerm_virtual_network.mexicocentralvnet.resource_group_name
  virtual_network_name = azurerm_virtual_network.mexicocentralvnet.name
  address_prefixes     = ["10.30.2.0/24"]
  }
resource "azurerm_subnet" "mexicocentralsubnet_test" {
  name                 = "subnet-test_${var.defaultlocation}"
  resource_group_name  = azurerm_virtual_network.mexicocentralvnet.resource_group_name
  virtual_network_name = azurerm_virtual_network.mexicocentralvnet.name
  address_prefixes     = ["10.30.3.0/24"]
  }
resource "azurerm_subnet" "expressroute1_subnet" {
  name                 = "GatewaySubnet"
  resource_group_name  = var.mexicocentralresourcegroups[0]
  virtual_network_name = azurerm_virtual_network.mexicocentralvnet.name
  address_prefixes     = ["10.30.254.0/24"]
}
