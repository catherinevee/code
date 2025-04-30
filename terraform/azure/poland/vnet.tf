module "avm-res-network-virtualnetwork" {
  source = "Azure/avm-res-network-virtualnetwork/azurerm"

  address_space       = [var.defaultvnet]
  location            = var.defaultlocation
  name                = join("_",[var.defaultlocation, var.defaultenv, "vnet"])
  resource_group_name = var.defaultrg
  subnets = {
    "subnet1" = {
      name             = "subnet1"
      address_prefixes = ["10.0.0.0/24"]
    }
    "subnet2" = {
      name             = "subnet2"
      address_prefixes = ["10.0.1.0/24"]
    }
  }
}