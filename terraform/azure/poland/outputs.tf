#
output "tfstate_storage_account_id" {
  value = "${data.azurerm_storage_account.tfstate_sa.id}"
}