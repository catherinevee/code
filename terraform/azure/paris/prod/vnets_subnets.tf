resource "azurerm_virtual_network" "euwest3-dev-vnet" {
  name                = "euwest3-dev-vnet"
  resource_group_name = azurerm_resource_group.euwest3-dev.name
  location = "northeurope"
  
  address_space = ["10.1.0.0/16"]

}

resource "azurerm_virtual_network" "euwest3-prod-vnet" {
  name                = "euwest3-prod-vnet"
  resource_group_name = azurerm_resource_group.euwest3-prod.name
  location = "northeurope"
  
  address_space = ["10.3.0.0/16"]

}

resource "azurerm_virtual_network" "euwest3-test-vnet" {
  name                = "euwest3-test-vnet"
  resource_group_name = azurerm_resource_group.euwest3-test.name
  location = "northeurope"
  
  address_space = ["10.2.0.0/16"]

}

resource "azurerm_subnet" "subnet-eu-west-3-1" {
  name                 = "subnet-eu-west-3-1"
  resource_group_name  = azurerm_resource_group.euwest3-dev.name
  virtual_network_name = azurerm_virtual_network.euwest3-dev-vnet.name
  address_prefixes     = ["10.0.101.0/24"]
}

resource "azurerm_subnet" "subnet-eu-west-3-2" {
  name                 = "subnet-eu-west-3-2"
  resource_group_name  = azurerm_resource_group.euwest3-dev.name
  virtual_network_name = azurerm_virtual_network.euwest3-dev-vnet.name
  address_prefixes     = ["10.0.102.0/24"]
}

resource "azurerm_subnet" "subnet-eu-west-3-3" {
  name                 = "subnet-eu-west-3-3"
  resource_group_name  = azurerm_resource_group.euwest3-test.name
  virtual_network_name = azurerm_virtual_network.euwest3-test-vnet.name
  address_prefixes     = ["10.0.103.0/24"]
}

resource "azurerm_subnet" "subnet-uswest-4" {
  name                 = "subnet-uswest-4"
  resource_group_name  = azurerm_resource_group.euwest3-prod.name
  virtual_network_name = azurerm_virtual_network.euwest3-prod-vnet.name
  address_prefixes     = ["10.0.104.0/24"]
}