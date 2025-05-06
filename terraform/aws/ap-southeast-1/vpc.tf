locals {
  
}


#these are used to re-use elastic ips instead of creating new ones 
resource "aws_eip" "nat" {
  count = 3

}



module "vpc" {
  source = "terraform-aws-modules/vpc/aws"

  name = var.defaultvpc
  cidr = var.defaultcidr

  azs             = var.defaultaz
  private_subnets = var.default_privatesubnets
  public_subnets  = var.default_publicsubnets

  enable_nat_gateway = true #per subnet
  #single_nat_gateway = true
  #one-nat-gateway-per-az = true
  enable_vpn_gateway = true
  reuse_nat_ips       = true         
  external_nat_ip_ids = "${aws_eip.nat.*.id}"
  tags = var.defaulttags
}

