module "avm-res-network-virtualnetwork"  {
  source = "Azure/avm-res-network-virtualnetwork/azurerm"

  address_space       = [var.defaultvnet]
  location            = var.defaultlocation
  name                = join("_",[var.defaultlocation, var.defaultenv, "vnet1"])
  resource_group_name = var.defaultrg
  subnets = {
    "subnet1" = {
      name             = "${defaultenv}subnet1"
      address_prefixes = ["10.0.2.0/24"]
    }
    "subnet2" = {
      name             = "${defaultenv}subnet2"
      address_prefixes = ["10.0.1.0/24"]
    }
  }
}

module "avm-res-network-virtualnetwork"  {
  source = "Azure/avm-res-network-virtualnetwork/azurerm"

  address_space       = ["10.1.0.0/16"]
  location            = var.defaultlocation
  name                = join("_",[var.defaultlocation, var.defaultenv, "vnet2"])
  resource_group_name = var.defaultrg
  subnets = {
    "subnet1" = {
      name             = "${defaultenv}subnet1"
      address_prefixes = ["10.1.2.0/24"]
    }
    "subnet2" = {
      name             = "${defaultenv}subnet2"
      address_prefixes = ["10.1.1.0/24"]
    }
  }
}