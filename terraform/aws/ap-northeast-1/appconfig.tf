
# Auto Scaling Group (conditional)
resource "aws_autoscaling_group" "app" {
  count               = var.app_config.features.auto_scaling ? 1 : 0
  name                = "${var.app_config.name}-asg"
  vpc_zone_identifier = data.aws_subnets.private.ids
  target_group_arns   = [aws_lb_target_group.app.arn]
  health_check_type   = "ELB"

  min_size         = var.app_config.scaling.min_instances
  max_size         = var.app_config.scaling.max_instances
  desired_capacity = var.app_config.scaling.min_instances

  launch_template {
    id      = aws_launch_template.app.id
    version = "$Latest"
  }

  tag {
    key                 = "Name"
    value               = "${var.app_config.name}-instance"
    propagate_at_launch = true
  }
}
