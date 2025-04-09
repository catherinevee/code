module "avm-res-keyvault-vault" {
  source  = "Azure/avm-res-keyvault-vault/azurerm"
  version = "0.10.0"
  location = var.defaultlocation
  name = "${var.defaultlocation}-keyvault"
  resource_group_name = var.defaultrg
  tenant_id = ""
  contacts = "catherine.vee@outlook.com"
}