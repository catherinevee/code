terraform {
  backend "azurerm" {
      resource_group_name  = "${var.tfstaterg}"
      storage_account_name = "${var.tfstatesa}"
      container_name       = "${var.tfstatecontainer}"
      key = "terraform.tfstate"
      #access_key = {{secrets.storagekey}}
      use_oidc = true
      use_azuread_auth = true
      client_id = "259e201e-2c35-46e1-9908-4e93331d6de5catherinevee_manid" 
  }
}