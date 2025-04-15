terraform {
  backend "azurerm" {
      resource_group_name  = "${var.tfstaterg}"
      storage_account_name = "${var.tfstatesa}"
      container_name       = "${var.tfstatecontainer}"
      key = "tf/terraform.tfstate"
      use_msi = true
      client_id = "catherinevee_manid"
      subscription_id = var.ARM_SUBSCRIPTION_ID
      tenant_id = var.AZURE_TENANT_ID      
  }
}