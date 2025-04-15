terraform {
  backend "azurerm" {
      resource_group_name  = "${var.tfstaterg}"
      storage_account_name = "${var.tfstatesa}"
      container_name       = "${var.tfstatecontainer}"
      key = "terraform.tfstate"
      access_key = "$(storagekey)"
      #use_msi = true
      #client_id = "catherinevee_manid" 
  }
}