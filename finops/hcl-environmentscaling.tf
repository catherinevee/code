# Variable-driven resource sizing based on environment
variable "environment_configs" {
  type = map(object({
    instance_type     = string
    min_capacity      = number
    max_capacity      = number
    multi_az          = bool
    backup_retention  = number
  }))

  default = {
    production = {
      instance_type     = "m5.xlarge"
      min_capacity      = 2
      max_capacity      = 10
      multi_az          = true
      backup_retention  = 30
    }
    staging = {
      instance_type     = "m5.large"
      min_capacity      = 1
      max_capacity      = 3
      multi_az          = false
      backup_retention  = 7
    }
    development = {
      instance_type     = "t3.medium"
      min_capacity      = 1
      max_capacity      = 2
      multi_az          = false
      backup_retention  = 1
    }
  }
}

# Use environment-specific configuration
locals {
  config = var.environment_configs[var.environment]
}

resource "aws_db_instance" "main" {
  identifier     = "${var.project}-${var.environment}"
  engine         = "postgres"
  engine_version = "13.7"
  instance_class = "db.${local.config.instance_type}"

  allocated_storage     = local.config.storage_size
  max_allocated_storage = local.config.max_storage_size

  multi_az               = local.config.multi_az
  backup_retention_period = local.config.backup_retention

  tags = local.common_tags
}
