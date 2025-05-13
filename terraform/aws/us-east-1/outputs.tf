output "output_defaultvpc_id" {
  value = module.vpc.default_vpc_id
}

output "output_subnet_ids" {
    value = values(vpc.private_subnets)[*].id
}