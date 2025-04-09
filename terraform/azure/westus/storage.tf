module "avm-res-storage-storageaccount" {
  source  = "Azure/avm-res-storage-storageaccount/azurerm"
  version = "0.5.0"
  location = var.defaultlocation
  name = "${var.defaultlocation}saprod"
  resource_group_name = var.defaultrg
  access_tier = "Cool"
  account_kind = "StorageV2"
  account_replication_type = "LRS"
  account_tier = "Standard"
}

