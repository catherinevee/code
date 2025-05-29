# Application Load Balancer (always created)

locals {
  is_production = var.app_config.environment == "production"
}

resource "aws_lb" "main" {
  name               = "${var.app_config.name}-${var.app_config.environment}"
  internal           = false
  load_balancer_type = "application"
  subnets            = data.aws_subnets.public.ids

  enable_deletion_protection = local.is_production
}
