
output "container_registry_name" {
  value = azurerm_container_registry.acr
}

output "container_registry_login_server" {
  value = azurerm_container_registry.acr.login_server
}