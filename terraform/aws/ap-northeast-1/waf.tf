locals {
  is_production = var.app_config.environment == "production"
  # Production gets enhanced features
  enable_waf = var.app_config.features.waf_protection && local.is_production
}



# WAF (only for production with feature enabled)
resource "aws_wafv2_web_acl" "main" {
  count = local.enable_waf ? 1 : 0
  name  = "${var.app_config.name}-waf"
  scope = "REGIONAL"

  default_action {
    allow {}
  }

  rule {
    name     = "rate-limit"
    priority = 1

    override_action {
      none {}
    }

    statement {
      rate_based_statement {
        limit              = 2000
        aggregate_key_type = "IP"
      }
    }

    visibility_config {
      cloudwatch_metrics_enabled = true
      metric_name                = "rateLimitRule"
      sampled_requests_enabled   = true
    }

    action {
      block {}
    }
  }

  visibility_config {
    cloudwatch_metrics_enabled = true
    metric_name                = "${var.app_config.name}WAF"
    sampled_requests_enabled   = true
  }
}