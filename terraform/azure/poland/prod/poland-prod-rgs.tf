#poland
resource "azurerm_resource_group" "poland-dev-resourcegroups" {
  location = "polandcentral"
  for_each = toset(var.poland-var-prodresourcegroups)
  name = each.value  
}

resource "azurerm_resource_group" "poland-dev-resourcegroup-polandprod4" {
  location = "polandcentral"
  name = "poland-dev-resourcegroup-polandprod4"
}
