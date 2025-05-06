resource "azurerm_public_ip" "lb_azurepublicip" {
  name                = "PublicIPForLB"
  location            = var.defaultlocation 
  resource_group_name = var.defaultrg
  allocation_method   = "Static"
}


resource "azurerm_lb" "lb_azurepubliclb" {
  name                = "cathyloadbalancer"
  location            = var.defaultlocation
  resource_group_name = var.defaultrg

  frontend_ip_configuration {
    name                 = "PublicIPAddress"
    public_ip_address_id = azurerm_public_ip.lb_azurepublicip.id
  }
}

resource "azurerm_lb_probe" "lb_probe" {
  loadbalancer_id = azurerm_lb.lb_azurepubliclb.id
  name            = "ssh-running-probe"
  port            = 22
}

resource "azurerm_lb_backend_address_pool" "lb_backendpool" {
  loadbalancer_id = azurerm_lb.lb_azurepubliclb.id
  name            = "backendaddresspool_publiclb"
}