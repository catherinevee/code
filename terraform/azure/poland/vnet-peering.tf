resource "azurerm_virtual_network_peering" "example-1" {
  name                      = "peer1to2"
  resource_group_name       = var.defaultrg
  virtual_network_name      = join("_",[var.defaultlocation, var.defaultenv, "vnet2"])
  remote_virtual_network_id = var.virtual_network_id2.id
}

resource "azurerm_virtual_network_peering" "example-2" {
  name                      = "peer2to1"
  resource_group_name       = var.defaultrg
  virtual_network_name      = join("_",[var.defaultlocation, var.defaultenv, "vnet1"])
  remote_virtual_network_id = var.virtual_network_id1.id
}