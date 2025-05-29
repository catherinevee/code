locals {
  # Combine environment and feature flags for complex conditions
  create_advanced_monitoring = var.features.monitoring && var.environment == "production"
}

resource "aws_cloudwatch_log_group" "app_logs" {
  count             = var.features.monitoring ? 1 : 0
  name              = "/aws/application/${var.environment}"
  retention_in_days = var.environment == "production" ? 30 : 7
}

resource "aws_cloudwatch_metric_alarm" "high_cpu" {
  count               = local.create_advanced_monitoring ? 1 : 0
  alarm_name          = "${var.environment}-high-cpu"
  comparison_operator = "GreaterThanThreshold"
  evaluation_periods  = "2"
  metric_name         = "CPUUtilization"
  namespace           = "AWS/EC2"
  period              = "120"
  statistic           = "Average"
  threshold           = "80"
  alarm_description   = "This metric monitors ec2 cpu utilization"
}
