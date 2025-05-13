output "output_defaultvpc_id" {
  value = module.vpc.name.id
}

output "output_subnet_ids" {
    value = values(module.vpc.private_subnets)[*].id
}