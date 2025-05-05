resource "azurerm_container_registry" "acr" {
  name                = var.defaultacr
  resource_group_name = var.defaultrg
  location            = var.defaultlocation
  sku                 = "standard"
}

resource "azurerm_role_assignment" "acr_roleassignment" {
  principal_id                     = azurerm_kubernetes_cluster.acr.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.defaultacr.id
  skip_service_principal_aad_check = true
}