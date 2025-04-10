module "avm-res-network-virtualnetwork" {
  source = "Azure/avm-res-network-virtualnetwork/azurerm"

  address_space       = ["10.0.0.0/16"]
  location            = "${var.defaultlocation}"
  name                = "${var.defaultlocation}"
  resource_group_name = var.defaultrg
  subnets = {
    "subnet1" = {
      name             = "${var.defaultlocation}-subnet1"
      address_prefixes = ["10.99.0.0/24"]
    }
    "subnet2" = {
      name             = "{${var.defaultlocation}-subnet2"
      address_prefixes = ["10.99.1.0/24"]
    }
  }
}