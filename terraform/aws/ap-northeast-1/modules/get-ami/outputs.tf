output "ami" {
  description = "SSM parameter resource containing the AMI data"
  value       = data.aws_ssm_parameter.this
  sensitive   = true
}

output "ami_id" {
  description = "AMI ID"
  value       = nonsensitive(data.aws_ssm_parameter.this.value)
}