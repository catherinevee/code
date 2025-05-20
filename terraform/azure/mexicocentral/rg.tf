resource "azurerm_resource_group" "polandcentral-prod-resourcegroups" {
  location = var.defaultlocation
  for_each = toset(var.mexicocentralresourcegroups)
  name = each.value  
}
