#this is used in monitor.tf, azurerm_monitor_metric_alert
output "tfstate_storage_account_id" {
  value = "${data.azurerm_storage_account.tfstate_sa.id}"
}

data "azurerm_virtual_network" "data_defaultvnet_id" {
 depends_on = [
    module.avm-res-network-virtualnetwork-vnet1
 ]
  name                = join("_",[var.defaultlocation, var.defaultenv, "vnet1"])
  resource_group_name = var.defaultrg
}

output "virtual_network1_id" {
  value = data.azurerm_virtual_network.data_defaultvnet_id.id
}


data "azurerm_virtual_network" "data_secondvnet_id" {
 depends_on = [
    module.avm-res-network-virtualnetwork-vnet2
 ]
  name                = join("_",[var.defaultlocation, var.defaultenv, "vnet2"])
  resource_group_name = var.defaultrg
}

output "virtual_network2_id" {
  value = data.azurerm_virtual_network.data_secondvnet_id
}


output "client_certificate" {
  value     = azurerm_kubernetes_cluster.poland-aks.kube_config[0].client_certificate
  sensitive = true
}

output "kube_config" {
  value = azurerm_kubernetes_cluster.poland-aks.kube_config_raw

  sensitive = true
}