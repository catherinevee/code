output "output_defaultvpc_id" {
  value = module.vpc.default_vpc_id
}

output "output_subnet_ids" {
    value = module.vpc.private_subnets.*
}

data "aws_subnets" "defaultvpc" {
  filter {
    name   = "vpc-id"
    values = [module.vpc.vpc_id]
  }
}

data "aws_subnet" "defaultsubnets" {
  for_each = toset(data.aws_subnets.defaultvpc.id)
  id       = each.value
}

output "subnet_cidr_blocks" {
  value = [for s in data.aws_subnet.defaultsubnets : s.ids]
}