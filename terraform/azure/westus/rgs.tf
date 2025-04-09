#poland
resource "azurerm_resource_group" "westus-prod-resourcegroups" {
  location = var.defaultlocation
  for_each = toset(var.westus-var-prodresourcegroups)
  name = each.value  
}

resource "azurerm_resource_group" "westus-dev-resourcegroups" {
  location = var.defaultlocation
  for_each = toset(var.westus-var-devresourcegroups)
  name = each.value 
}
