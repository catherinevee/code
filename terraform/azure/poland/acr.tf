resource "azurerm_container_registry" "acr" {
  name                = var.defaultacr
  resource_group_name = var.defaultrg
  location            = var.defaultlocation
  sku                 = "Standard"
}

resource "azurerm_role_assignment" "acr_roleassignment" {
  depends_on = [
     azurerm_container_registry.acr,
     azurerm_kubernetes_cluster.poland-aks
   ]
  principal_id                     = azurerm_kubernetes_cluster.poland-aks.kubelet_identity[0].object_id
  role_definition_name             = "AcrPull"
  scope                            = azurerm_container_registry.acr.id
  skip_service_principal_aad_check = true
}