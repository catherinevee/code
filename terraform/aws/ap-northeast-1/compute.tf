resource "aws_instance" "app_servers" {
  for_each      = var.environments
  ami           = data.aws_ami.ubuntu.id
  instance_type = each.value.instance_type

  tags = {
    Name        = "${each.key}-app-server"
    Environment = each.key
  }
}