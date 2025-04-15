terraform {
  backend "azurerm" {
      resource_group_name  = "${var.defaultrg}"
      storage_account_name = "${var.defaultsa}"
      container_name       = "${var.defaultsa-container}"
      use_msi = true
      client_id = "catherinevee_manid"

  }
}