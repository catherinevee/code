data "azurerm_client_config" "current" {}

resource "azurerm_key_vault" "des_vault" {
  location                    = var.defaultlocation
  name                        = "${var.defaultlocation}keyvault"
  resource_group_name         = var.defaultrg
  sku_name                    = "standard"
  tenant_id                   = data.azurerm_client_config.current.tenant_id
  enabled_for_disk_encryption = true
  purge_protection_enabled    = true
  soft_delete_retention_days  = 7
}