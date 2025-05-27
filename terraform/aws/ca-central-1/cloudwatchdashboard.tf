resource "aws_cloudwatch_dashboard" "app_dashboard" {
  count          = var.create_monitoring ? 1 : 0
  dashboard_name = "application-metrics"

  dashboard_body = jsonencode({
    widgets = [
      {
        type   = "metric"
        width  = 12
        height = 6
        properties = {
          metrics = [
            ["AWS/ApplicationELB", "RequestCount"]
          ]
          region = "us-west-2"
          title  = "Request Count"
        }
      }
    ]
  })
}
