# terraform.tfvars
environments = {
  staging = {
    instance_type = "t3.small"
    enable_https  = true
    backup_days   = 7  # Backup volume created
  }
}

app_config = {
  name        = "starrez"
  environment = "staging"
  domain      = "staging.catherine.it.com"
  features = {
    https_redirect   = false
    waf_protection  = false
    auto_scaling    = false
    database_backup = false
    monitoring      = false
  }
  scaling = {
    min_instances = 1
    max_instances = 2
    target_cpu    = 80
  }
}

security_rules = {
  allow_http  = true
  allow_https = false
  allow_ssh   = true
  ssh_cidrs   = ["10.101.0.0/0"]  # Open SSH for development
}