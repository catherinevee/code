
output "express_route_circuit_id" {
  value = azurerm_express_route_circuit.expressroute1_circuit.id
}

output "gateway_name" {
  value = azurerm_virtual_network_gateway.expressroute1_ergateway.name
}

output "gateway_ip" {
  value = azurerm_public_ip.gateway_ip.ip_address
}

output "service_key" {
  value     = azurerm_express_route_circuit.expressroute1_circuit.service_key
  sensitive = true
}