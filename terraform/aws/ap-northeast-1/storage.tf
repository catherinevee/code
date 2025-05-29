
resource "aws_ebs_volume" "backup_storage" {
  for_each = {
    for env, config in var.workstations : env => config
    if config.backup_days > 0
  }

  availability_zone = aws_instance.app_servers[each.key].availability_zone
  size             = 20

  tags = {
    Name = "${each.key}-backup-volume"
  }
}