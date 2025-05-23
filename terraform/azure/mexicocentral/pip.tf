# Azure Public IP Address for the VNet Gateway
resource azurerm_public_ip "vnet_gateway_public_ip" {
    name                  = "${var.defaultlocation}-vgw-pip"
    resource_group_name   = var.mexicocentralresourcegroups[0]
    location              = var.defaultlocation

    sku               = "Basic"
    allocation_method = "Dynamic"
}