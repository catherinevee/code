#paris
resource "azurerm_resource_group" "euwest3-dev-resourcegroups" {
  location = "northeurope"
  for_each = toset(var.dev_environment_type)
  name = each.value  
}

resource "azurerm_resource_group" "euwest3-dev" {
  name     = "euwest3-dev"
  location = "northeurope"
}

resource "azurerm_resource_group" "euwest3-prod" {
  name     = "euwest3-prod"
  location = "northeurope"


}
resource "azurerm_resource_group" "euwest3-test" {
  name     = "euwest3-test"
  location = "northeurope"
}