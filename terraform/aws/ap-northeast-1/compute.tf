module "ubuntu_24_04_latest" {
  source = "modules/get-ami"
}

locals {
  ami_id = module.ami_ubuntu_24_04_latest.ami.image_id
}

## --> use `local.ami_id

resource "aws_instance" "app_servers" {
  for_each      = var.workstations
  ami           = local.ami_id
  instance_type = each.value.instance_type

  tags = {
    Name        = "${each.key}-app-server"
    Environment = each.key
  }
}