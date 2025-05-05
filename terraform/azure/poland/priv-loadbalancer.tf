module "mylb" {
  source                                 = "Azure/loadbalancer/azurerm"
  resource_group_name                    = var.defaultrg
  type                                   = "private"
  frontend_subnet_id                     = module.avm-res-network-virtualnetwork-vnet2.subnets[0].id
  frontend_private_ip_address_allocation = "Static"
  frontend_private_ip_address            = "10.1.2.254"
  lb_sku                                 = "Standard"
  pip_sku                                = "Standard"

  remote_port = {
    ssh = ["Tcp", "22"]
  }

  lb_port = {
    http  = ["80", "Tcp", "80"]
    https = ["443", "Tcp", "443"]
  }

  lb_probe = {
    http  = ["Tcp", "80", ""]
    http2 = ["Http", "1443", "/"]
  }

  tags = {
    cost-center = "12345"
    source      = "terraform"
  }
}