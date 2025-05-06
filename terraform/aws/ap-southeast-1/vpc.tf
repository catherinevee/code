module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.defaultvpc
  cidr = var.defaultcidr

  azs             = var.defaultaz
  private_subnets = var.default_privatesubnets
  public_subnets  = var.default_publicsubnets

  enable_nat_gateway = true
  enable_vpn_gateway = true

  tags = var.defaulttags
}