locals {
  ami_param = "/aws/service/canonical/ubuntu/server/${var.ubuntu_version}/stable/current/${var.arch}/${var.virtualization_type}/${var.volume_type}/ami-id"
}

data "aws_ssm_parameter" "this" {
  name = local.ami_param
}