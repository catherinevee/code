resource "azurerm_log_analytics_workspace" "poland-compute-analytics-ws" {
  name                = var.defaultanalyticsworkspace
  location            = var.defaultlocation
  resource_group_name = var.defaultrg
  sku                 = "PerGB2018"
  retention_in_days   = 1
}

resource "azurerm_container_app_environment" "poland-containerappenv" {
  name                       = var.defaultcontainerappenv
  location            = var.defaultlocation
  resource_group_name = var.defaultrg
  log_analytics_workspace_id = azurerm_log_analytics_workspace.poland-compute-analytics-ws.id
}

resource "azurerm_container_app" "poland-containerapp" {
  name                         = var.defaultcontainerapp
  container_app_environment_id = azurerm_container_app_environment.poland-containerappenv.id
  resource_group_name          = var.defaultrg
  revision_mode                = "Single"

  template {
    max_replicas = 3
    container {
      name   = "examplecontainerapp"
      image  = "mcr.microsoft.com/k8se/quickstart:latest"
      cpu    = 0.25
      memory = "0.5Gi"
    
      readiness_probe {
        transport = "HTTP"
        port      = 80
      }

      liveness_probe {
        transport = "HTTP"
        port      = 80
      }

      startup_probe {
        transport = "HTTP"
        port      = 80
      }   
    } 
  }
}