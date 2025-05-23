locals {
  location_alias = "mexico"
  env = "prod"
  prefix = "${local.location_alias}-${local.env}-"
}

resource "random_string" "random" {
  length           = 16
  special          = true
  override_special = "/@£$"
}


resource "azurerm_public_ip" "gateway_ip" {
  name                 = "pip-${random_string.random.result}"
  location            = var.defaultlocation
  resource_group_name = var.mexicocentralresourcegroups[0]
  allocation_method   = "Static"
  sku                 = "Standard"
}


resource "azurerm_virtual_network_gateway" "expressroute1_ergateway" {
  name                = "${local.prefix}ergateway"
  resource_group_name = var.mexicocentralresourcegroups[0]
  location            = var.defaultlocation
  type                = "ExpressRoute"
  vpn_type            = "RouteBased"
  active_active       = false
  enable_bgp          = false
  sku                 = "HighPerformance"

  ip_configuration {
    name                 = "vnetExpRouteGatewayConfig"
    public_ip_address_id = azurerm_public_ip.gateway_ip.id
    subnet_id            = azurerm_subnet.expressroute1_subnet.id
  }
  tags = var.tags

}


resource "azurerm_express_route_port" "expressroute1_port" {
  name                = "${local.prefix}erport"
  resource_group_name = var.mexicocentralresourcegroups[0]
  location            = var.defaultlocation
  peering_location    = "Alestra-A-1-LWQ"
  bandwidth_in_gbps   = 1
  encapsulation       = "Dot1Q"
}

resource "azurerm_express_route_circuit" "expressroute1_circuit" {
  name                  = "${local.prefix}ercircuit"
  location              = var.defaultlocation
  service_provider_name = "Alestra"
  peering_location    = var.defaultlocation
  bandwidth_in_mbps   = 1024
  resource_group_name   = var.mexicocentralresourcegroups[0]
  express_route_port_id = azurerm_express_route_port.expressroute1_port.id

  sku {
    tier   = "Standard"
    family = "MeteredData"
  }
}


resource "azurerm_express_route_circuit_peering" "expressroute1_circuitpeering" {
  peering_type                  = "AzurePrivatePeering"
  express_route_circuit_name    = azurerm_express_route_circuit.expressroute1_circuit.name
  resource_group_name           = var.mexicocentralresourcegroups[0]
  peer_asn                      = 191
  primary_peer_address_prefix   = "192.168.10.16/30"
  secondary_peer_address_prefix = "192.168.10.20/30"
  vlan_id                       = 1200
}
