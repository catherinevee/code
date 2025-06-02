# Enhanced Terraform module with cost optimization built-in
# terraform/modules/cost-aware-web-app/main.tf

variable "environment" {
  description = "Environment name (dev, staging, prod)"
  type        = string
}

variable "expected_users" {
  description = "Expected number of daily active users"
  type        = number
}

variable "cost_budget" {
  description = "Monthly cost budget in USD"
  type        = number
}

# Cost-aware configuration based on environment and budget
locals {
  environment_configs = {
    dev = {
      instance_type     = "t3.small"
      min_size         = 1
      max_size         = 2
      enable_spot      = true
      storage_type     = "gp3"
      multi_az         = false
    }
    staging = {
      instance_type     = "t3.medium"
      min_size         = 1
      max_size         = 3
      enable_spot      = true
      storage_type     = "gp3"
      multi_az         = false
    }
    prod = {
      instance_type     = "m5.large"
      min_size         = 2
      max_size         = 10
      enable_spot      = false
      storage_type     = "gp3"
      multi_az         = true
    }
  }

  config = local.environment_configs[var.environment]

  # Calculate if we need to adjust for budget constraints
  estimated_monthly_cost = local.config.min_size * 730 * 0.096  # Rough calculation
  needs_cost_optimization = local.estimated_monthly_cost > var.cost_budget

  # Adjust configuration if over budget
  final_config = local.needs_cost_optimization ? {
    instance_type = var.environment == "prod" ? "t3.large" : "t3.small"
    min_size     = 1
    max_size     = local.config.max_size
    enable_spot  = var.environment != "prod" ? true : local.config.enable_spot
    storage_type = "gp3"
    multi_az     = var.environment == "prod" ? true : false
  } : local.config
}

# Auto Scaling Group with cost-optimized configuration
resource "aws_autoscaling_group" "web" {
  name                = "${var.environment}-web-asg"
  vpc_zone_identifier = var.subnet_ids
  target_group_arns   = [aws_lb_target_group.web.arn]
  health_check_type   = "ELB"

  min_size         = local.final_config.min_size
  max_size         = local.final_config.max_size
  desired_capacity = local.final_config.min_size

  # Use mixed instances policy for cost optimization
  mixed_instances_policy {
    launch_template {
      launch_template_specification {
        launch_template_id = aws_launch_template.web.id
        version           = "$Latest"
      }

      # Cost optimization: Use multiple instance types
      override {
        instance_type = local.final_config.instance_type
      }

      # Add spot instances for non-production
      dynamic "override" {
        for_each = local.final_config.enable_spot ? [1] : []
        content {
          instance_type = local.final_config.instance_type
          spot_max_price = "0.05"  # Set maximum spot price
        }
      }
    }

    instances_distribution {
      on_demand_base_capacity                  = var.environment == "prod" ? 1 : 0
      on_demand_percentage_above_base_capacity = var.environment == "prod" ? 50 : 0
      spot_allocation_strategy                 = "diversified"
    }
  }

  # Enhanced tagging for cost attribution
  tag {
    key                 = "Name"
    value               = "${var.environment}-web-server"
    propagate_at_launch = true
  }

  tag {
    key                 = "Environment"
    value               = var.environment
    propagate_at_launch = true
  }

  tag {
    key                 = "CostCenter"
    value               = "engineering"
    propagate_at_launch = true
  }

  tag {
    key                 = "ExpectedUsers"
    value               = var.expected_users
    propagate_at_launch = true
  }

  tag {
    key                 = "CostBudget"
    value               = var.cost_budget
    propagate_at_launch = true
  }
}

# Cost monitoring and alerting
resource "aws_cloudwatch_metric_alarm" "cost_budget_alarm" {
  alarm_name          = "${var.environment}-cost-budget-alarm"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "1"
  metric_name         = "EstimatedCharges"
  namespace           = "AWS/Billing"
  period              = "86400"
  statistic           = "Maximum"
  threshold           = var.cost_budget * 0.8  # Alert at 80% of budget
  alarm_description   = "Cost approaching budget limit"

  dimensions = {
    Currency = "USD"
  }

  alarm_actions = [aws_sns_topic.cost_alerts.arn]
}

# Output cost estimation for transparency
output "estimated_monthly_cost" {
  description = "Estimated monthly cost for this configuration"
  value = {
    base_cost = local.estimated_monthly_cost
    optimized = local.needs_cost_optimization
    final_estimate = local.needs_cost_optimization ? local.estimated_monthly_cost * 0.7 : local.estimated_monthly_cost
  }
}
