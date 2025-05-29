# terraform.tfvars
workstations = {
  development = {
    instance_type = "t3.micro"
    enable_https  = false
    backup_days   = 0  # No backup volume created
  }
}

app_config = {
  name        = "starrez"
  environment = "development"
  domain      = "dev.catherine.it.com"
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
  allow_https = true
  allow_ssh   = true
  ssh_cidrs   = var.default_privatesubnets[0]  # Only internal networks
}

