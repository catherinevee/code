
locals {
  tgw_name = join("_",["tgw_",var.defaultregion,"_to_",var.peer_defaultregion])

}


################################################################################
# VPC modules
################################################################################

module "vpc1" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"

  name = var.defaultvpc
  cidr = var.defaultcidr

  azs             = var.defaultaz
  private_subnets = var.default_publicsubnets

  enable_ipv6                                    = false
  tags = var.defaulttags
}


module "vpc2" {
  source  = "terraform-aws-modules/vpc/aws"
  version = "~> 5.0"



  name = var.peer_defaultvpc
  cidr = var.peer_defaultcidr

  azs             = var.peer_defaultaz
  private_subnets = var.peer_defaultprivatesubnets

  enable_ipv6 = false

  tags = var.peer_defaulttags
}


################################################################################
# Transit Gateway Module
################################################################################

module "tgw" {
  source  = "terraform-aws-modules/transit-gateway/aws"
  version = "2.13.0"
  name            = local.tgw_name
  description     = "Transit Gateway, Multi-account"
  amazon_side_asn = 64532

  # When "true" there is no need for RAM resources if using multiple AWS accounts
  enable_auto_accept_shared_attachments = true

  vpc_attachments = {
    vpc1 = {
      vpc_id       = module.vpc1.vpc_id
      subnet_ids   = module.vpc1.private_subnets
      dns_support  = true
      ipv6_support = true

      transit_gateway_default_route_table_association = false
      transit_gateway_default_route_table_propagation = false

      tgw_routes = [
        {
          destination_cidr_block = "30.0.0.0/16"
        },
        {
          blackhole              = true
          destination_cidr_block = "0.0.0.0/0"
        }
      ]
    },
    vpc2 = {
      vpc_id     = module.vpc2.vpc_id
      subnet_ids = module.vpc2.private_subnets

      tgw_routes = [
        {
          destination_cidr_block = "50.0.0.0/16"
        },
        {
          blackhole              = true
          destination_cidr_block = "10.10.10.10/32"
        }
      ]
    },
  }

  #ram_allow_external_principals = true
  #ram_principals                = [307990089504]

  tags = var.defaulttags
}

module "tgw_peer" {
  # This is optional and connects to another account. Meaning you need to be authenticated with 2 separate AWS Accounts
  source  = "terraform-aws-modules/transit-gateway/aws"
  version = "2.13.0"

  name            = "${local.tgw_name}-peer"
  description     = "My TGW shared with several other AWS accounts"
  amazon_side_asn = 64532

  create_tgw             = false
  share_tgw              = true
  ram_resource_share_arn = module.tgw.ram_resource_share_id
  # When "true" there is no need for RAM resources if using multiple AWS accounts
  enable_auto_accept_shared_attachments = true

  vpc_attachments = {
    vpc1 = {
      tgw_id       = module.tgw.ec2_transit_gateway_id
      vpc_id       = module.vpc1.vpc_id
      subnet_ids   = module.vpc1.private_subnets
      dns_support  = true
      ipv6_support = true

      transit_gateway_default_route_table_association = false
      transit_gateway_default_route_table_propagation = false

      vpc_route_table_ids  = module.vpc1.private_route_table_ids
      tgw_destination_cidr = "0.0.0.0/0"

      tgw_routes = [
        {
          destination_cidr_block = "30.0.0.0/16"
        },
        {
          blackhole              = true
          destination_cidr_block = "0.0.0.0/0"
        }
      ]
    },
  }

  #ram_allow_external_principals = true
  #ram_principals                = [307990089504]

  tags = var.defaulttags
}
