terraform {
  backend "azurerm" {
      resource_group_name  = "${var.tfstaterg}"
      storage_account_name = "${var.tfstatesa}"
      container_name       = "${var.tfstatecontainer}"
      key = "terraform.tfstate"
      #access_key = {{secrets.storagekey}}
      use_oidc = true
      use_azuread_auth = true
      client_id = "catherinevee_manid" 
      tenant_id = var.AZURE_TENANT_ID
      subscription_id = var.ARM_SUBSCRIPTION_ID

  }
}