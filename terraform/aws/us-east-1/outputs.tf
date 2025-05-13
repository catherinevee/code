output "output_defaultvpc_id" {
  value = module.vpc.id
}

output "output_subnet_ids" {
    value = values(module.vpc.private_subnets)[*].id
}