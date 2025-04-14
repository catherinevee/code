terraform {
  backend "azurerm" {
      resource_group_name  = "${var.defaultrg}"
      storage_account_name = "${var.defaultsa}"
      container_name       = "${var.defaultsa-container}"
      key                  = "${var.ARM_ACCESS_KEY}"
      use_msi = true
      client_id = "catherinevee_manid"

  }
}