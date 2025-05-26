resource "aws_instance" "this" {
   count         = length(var.polandcentral-var-instances)
   instance_type = "t2.micro"
   ami           = "amiid"
   tags = {
       Name = var.polandcentral-var-instances[count.index]
   }
}

# Create a Manged Instance
resource "spotinst_managed_instance_aws" "default-managed-instance" {
  name        = "default-managed-instance"
  description = "created by Terraform"
  product     = "Linux/UNIX" #"Red Hat Enterprise Linux"

  region     = "us-west-2"
  subnet_ids = ["subnet-123"]
  vpc_id     = "vpc-123"

  life_cycle                 = "on_demand"
  orientation                = "balanced"
  draining_timeout           = "120"
  fallback_to_ondemand       = false
  utilize_reserved_instances = false
  optimization_windows       = ["Mon:03:00-Wed:02:20"]
  auto_healing               = "true"
  grace_period               = "180"
  unhealthy_duration         = "60"
  minimum_instance_lifetime  = "1"
  revert_to_spot {
    perform_at = "always"
  }

  persist_private_ip    = "true"
  persist_block_devices = "true"
  persist_root_device   = "true"
  block_devices_mode    = "reattach"
  health_check_type     = "EC2"

  #elastic_ip = "ip"
  #private_ip = "ip"

  instance_types = [
    "t1.micro",
    "t2.medium",
    "t2.large",
  ]

  preferred_type       = "t1.micro"
  #ebs_optimized        = "true"
  #enable_monitoring    = "true"
  placement_tenancy    = "default"
  image_id             = "ami-1234"
  #security_group_ids   = ["sg-234"]
  key_pair             = "labs-oregon"
  cpu_credits          = "standard"

  resource_requirements {
    excluded_instance_families = ["a", "m"]
    excluded_instance_types= ["m3.large"]
    #excluded_instance_generations= ["1", "2"]
    #required_gpu_minimum = 1
    #required_gpu_maximum = 16
    #required_memory_minimum = 2
    #required_memory_maximum = 512
    #required_vcpu_minimum = 2
    #required_vcpu_maximum = 64
  }


  block_device_mappings {
    device_name = "/dev/xvdcz"
    ebs {
      delete_on_termination = "true"
      volume_type           = "gp3"
      volume_size           = 50
      throughput            = 125
      encrypted             = true
      kms_key_id            = "kms-key-01"
      snapshot_id           = "snapshot_id"
    }
  }


}