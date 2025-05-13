output "output_defaultvpc_id" {
  value = module.vpc.default_vpc_id
}

output "output_subnet_ids" {
    value = module.vpc.private_subnets.*
}