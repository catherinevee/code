
resource "azurerm_kubernetes_cluster" "aks-cluster" {
  name                = var.defaultaks_clustername
  location            = var.defaultlocation
  resource_group_name = var.defaultrg
  dns_prefix          = "catherine92810293"

  default_node_pool {
    name       = "default"
    node_count = 1
    vm_size    = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags
}