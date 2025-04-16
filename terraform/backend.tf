terraform {
  backend "azurerm" {
      resource_group_name  = "polandcentralrg-1"
      storage_account_name = "tfstatecfriy"
      container_name       = "tfstate-container"
      key = "terraform.tfstate"
      access_key = "__storagekey__"
      #use_oidc = true
      #use_azuread_auth = true
      #client_id = "catherinevee_manid" 
      #tenant_id = var.AZURE_TENANT_ID
      #subscription_id = var.ARM_SUBSCRIPTION_ID

  }
}