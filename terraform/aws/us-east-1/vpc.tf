module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = "vpc-${var.defaultenv}"
  cidr = var.defaultvpc

  azs              = var.defaultaz
  private_subnets  = var.default_privatesubnets
  public_subnets   = var.default_publicsubnets

  enable_nat_gateway = true

  enable_ipv6                                   = true
  public_subnet_assign_ipv6_address_on_creation = true

  public_subnet_ipv6_prefixes   = [0, 1, 2]
  private_subnet_ipv6_prefixes  = [3, 4, 5]

  tags = var.defaulttags
}