# terraform/modules/scheduled_scaling/main.tf
resource "aws_autoscaling_schedule" "scale_down_evening" {
  count = var.environment == "development" ? 1 : 0

  scheduled_action_name  = "scale-down-evening"
  min_size               = 0
  max_size               = 0
  desired_capacity       = 0
  recurrence             = "0 18 * * MON-FRI"  # 6 PM weekdays
  autoscaling_group_name = aws_autoscaling_group.main.name
}

resource "aws_autoscaling_schedule" "scale_up_morning" {
  count = var.environment == "development" ? 1 : 0

  scheduled_action_name  = "scale-up-morning"
  min_size               = var.min_capacity
  max_size               = var.max_capacity
  desired_capacity       = var.desired_capacity
  recurrence             = "0 8 * * MON-FRI"   # 8 AM weekdays
  autoscaling_group_name = aws_autoscaling_group.main.name
}

# Lambda function for more complex scheduling logic
resource "aws_lambda_function" "resource_scheduler" {
  filename         = "resource_scheduler.zip"
  function_name    = "resource-scheduler"
  role            = aws_iam_role.scheduler.arn
  handler         = "index.handler"
  runtime         = "python3.9"
  timeout         = 300

  environment {
    variables = {
      ENVIRONMENT = var.environment
    }
  }
}

# CloudWatch rule to trigger the scheduler
resource "aws_cloudwatch_event_rule" "scheduler" {
  name                = "resource-scheduler"
  description         = "Trigger resource scheduler"
  schedule_expression = "cron(0 8,18 * * MON-FRI)"
}

resource "aws_cloudwatch_event_target" "lambda" {
  rule      = aws_cloudwatch_event_rule.scheduler.name
  target_id = "ResourceSchedulerTarget"
  arn       = aws_lambda_function.resource_scheduler.arn
}
