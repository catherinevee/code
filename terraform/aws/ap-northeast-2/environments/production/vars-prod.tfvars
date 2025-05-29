# terraform.tfvars
environments = {
  production = {
    instance_type = "t3.large"
    enable_https  = true
    backup_days   = 30  # Backup volume created
  }
}

app_config = {
  name        = "starrez"
  environment = "production"
  domain      = "prod.catherine.it.com"
  features = {
    https_redirect   = true
    waf_protection  = true
    auto_scaling    = true
    database_backup = true
    monitoring      = true
  }
  scaling = {
    min_instances = 3
    max_instances = 10
    target_cpu    = 70
  }
}


security_rules = {
  allow_http  = false
  allow_https = true
  allow_ssh   = false
}