resource "azurerm_virtual_wan" "mexicocentralvwan" {
  name                = "mexico-prod1-virtualwan"
  resource_group_name = var.mexicocentralresourcegroups[0]
  location            = var.defaultlocation
}

resource "azurerm_virtual_hub" "mexicocentralvhub" {
  name                = "mexico-prod1-vhub"
  resource_group_name = var.mexicocentralresourcegroups[0]
  location            = var.defaultlocation
  virtual_wan_id      = azurerm_virtual_wan.mexicocentralvwan.id
  address_prefix      = "10.0.1.0/24"
}
