terraform {
  backend "azurerm" {
      resource_group_name  = "${var.tfstateregion}"
      storage_account_name = "${var.tfstatesa}"
      container_name       = "${var.tfstatecontainer}"
      key = "tf/terraform.tfstate"
      use_msi = true
      #client_id = "catherinevee_manid"
      access_key = "${{secrets.AZURE_SA_TFSTATE_KEY}}"
  }
}