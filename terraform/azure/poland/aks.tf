
resource "azurerm_kubernetes_cluster" "poland-aks" {
  name                = var.defaultaks_clustername
  location            = var.defaultlocation
  resource_group_name = var.defaultrg
  dns_prefix          = var.defaultaks_dnsname

  default_node_pool {
    name       = "defaultprod"
    node_count = 3
    vm_size    = "Standard_D2_v2"
  }

  identity {
    type = "SystemAssigned"
  }

  tags = var.tags

