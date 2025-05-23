locals {
  location_alias = "mexico"
  env = "prod"
  prefix = "${local.location_alias}-${local.env}-" #{region}-{org}-{env}-{app}
}
resource "random_string" "random" {
  length           = 16
  special          = true
  override_special = "/@£$"

}
# Create the Azure ExpressRoute Circuit
resource azurerm_express_route_circuit "express_route" {
    name                  = "${prefix}-erc"
    resource_group_name   = var.mexicocentralresourcegroups[0]
    location              = var.defaultlocation

    # https://docs.microsoft.com/en-us/azure/expressroute/expressroute-locations-providers
    service_provider_name = "Alestra"
    peering_location      = "Mexico"
    bandwidth_in_mbps     = 1000

    sku {
        tier   = "Standard"  
        family = "MeteredData" 
    }
}

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
#======================================
#atp ExpressRoute circuit is awaiting authorization from ER provider
#
#Gather ER service key, give to ER provider
#======================================

# Azure ExpressRoute Private Peering
#this is to authorize the ER circuit to connect to Azure resources
resource azurerm_express_route_circuit_peering "express_route_peering" {
    resource_group_name           = var.mexicocentralresourcegroups[0]
    express_route_circuit_name    = azurerm_express_route_circuit.express_route.name

    peering_type                  = "AzurePrivatePeering"
    primary_peer_address_prefix   = "10.99.99.0/30"
    secondary_peer_address_prefix = "10.99.99.4/30"
    vlan_id                       = 100
}

#!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
# GatewaySubnet within the Virtual Network 
#resource azurerm_subnet "gateway_subnet" {
#    name                 = "GatewaySubnet"
#    ...
#}



# Azure Virtual Network Gateway
#create as an ExpressRoute gateway
resource azurerm_virtual_network_gateway "virtual_network_gateway" {
    name                = "${local.prefix}-vgw"
    location            = var.defaultlocation
    resource_group_name = var.mexicocentralresourcegroups[0]

    type     = "ExpressRoute"
    vpn_type = "PolicyBased"

    sku           = "HighPerformance"
    active_active = false
    enable_bgp    = false

    ip_configuration {
        name                          = "default"
        private_ip_address_allocation = "Dynamic"
        subnet_id                     = azurerm_subnet.expressroute1_subnet.id
        public_ip_address_id          = azurerm_public_ip.vnet_gateway_public_ip.id
    }
}

# connect the ExpressRoute Gateway to the ExpressRoute circuit
resource azurerm_virtual_network_gateway_connection "virtual_network_gateway_connection" {
    name                = "${local.prefix}-vgw-con"
    location            = var.defaultlocation
    resource_group_name = var.mexicocentralresourcegroups[0]

    type                            = "ExpressRoute"
    virtual_network_gateway_id      = azurerm_virtual_network_gateway.virtual_network_gateway.id
    express_route_circuit_id        = azurerm_express_route_circuit.express_route.id
}