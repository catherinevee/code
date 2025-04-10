#poland
resource "azurerm_resource_group" "polandcentral-prod-resourcegroups" {
  location = var.defaultlocation
  for_each = toset(var.polandcentral-var-prodresourcegroups)
  name = each.value  
}
