resource "azurerm_resource_group" "mexicocentralresourcegroups" {
  location = var.defaultlocation
  for_each = toset(var.mexicocentralresourcegroups)
  name = each.value  
}
