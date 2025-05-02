resource "azurerm_cost_anomaly_alert" "poland-costanomalyalert" {
  name            = "${var.defaultlocation}costanomalyalert"
  display_name    = "${var.defaultlocation}costanomalyalert"
  #subscription_id = 
  email_subject   = "Cost Anomaly Alert - ${var.defaultlocation}"
  email_addresses = ["${var.defaultemail}"]
}



resource "azurerm_monitor_action_group" "poland-monitoractiongroup" {
  name                = "${var.defaultlocation}monitoractiongroup"
  resource_group_name = "${var.defaultrg}"
  short_name          = "${var.defaultlocation}monitoractiongroup"
  email_receiver {
    name = "${var.defaultname}"
    email_address = "${var.defaultemail}"
  }
  webhook_receiver {
    name        = "cathytest"
    service_uri = "http://littorio.cath.net/alert"
  }
}


data "azurerm_storage_account" "tfstate_sa" {
  name                = "${var.tfstate_storageaccount}"
  resource_group_name = "${var.tfstate_storageaccount_rg}"
}

resource "azurerm_monitor_metric_alert" "poland-monitormetricalert" {
  name                = "${var.defaultlocation}metricalert"
  resource_group_name = "${var.defaultrg}"
  scopes              = [data.azurerm_storage_account.tfstate_sa.id]
  description         = "Action will be triggered when Transactions count is greater than 50."

  criteria {
    metric_namespace = "Microsoft.Storage/storageAccounts"
    metric_name      = "Transactions"
    aggregation      = "Total"
    operator         = "GreaterThan"
    threshold        = 50

    dimension {
      name     = "ApiName"
      operator = "Include"
      values   = ["*"]
    }
  }

  action {
    action_group_id = azurerm_monitor_action_group.poland-monitoractiongroup.id
  }
}