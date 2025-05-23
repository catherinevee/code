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

module "express_route" {
  source  = "claranet/expressroute/azurerm"
  version = "8.0.0"

  environment    = var.defaultenv
  location       = module.azure_region.location
  location_short = module.azure_region.location_short
  client_name    = "Alestra"
  stack          = "dev"

  resource_group_name = module.rg.name

  logs_destinations_ids = [
    module.logs.id
  ]

  service_provider_name = "Alestra"
  peering_location      = "Mexico Central"
  bandwidth_in_mbps     = 1024

  virtual_network_name = module.azure_virtual_network.name
  subnet_cidrs         =  ["${azurerm_subnet.expressroute1_subnet}"]

  # Enable when the ExpressRoute Circuit status is provisioned
  circuit_peering_enabled = false
  circuit_peerings = [
    {
      peering_type                  = "AzurePrivatePeering"
      primary_peer_address_prefix   = "169.254.0.0/30"
      secondary_peer_address_prefix = "169.254.0.4/30"
      peer_asn                      = 25419
      vlan_id                       = 100
    }
  ]
}