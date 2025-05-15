
variable "defaultregion" {
    type = string
    default = "us-west-1"
}

variable "defaulttags" {
  description = "Common tags for all resources"
  type = object({
    Environment = string
    OU   = string
  })
  default = {
    Environment = "prod"
    OU   = "IT"
  }
}


variable "defaultaz" {
    type = list(string)
    default = [
      "usw1-az1",
      "usw1-az2",
      "usw1-az3"
    ]
}

variable "defaultenv" {
    type = string
    default = "prod"
}

variable "defaultvpc" {
    type = string
    default = "10.20.0.0/16"
}

variable "default_privatesubnets" {
    type = list(string)
    default = [
      "10.20.1.0/24",
      "10.20.2.0/24",
      "10.20.3.0/24",
    ]
}

variable "default_publicsubnets" {
    type = list(string)
    default = [
      "10.20.10.0/24",
      "10.20.20.0/24",
      "10.20.30.0/24",
    ]
}

#===================
variable "default_eks" {
  type = string
  default = "eks-catherinecluster"
}

variable "default_eks-nodegroup" {
  type = string
  default = "eks-catherinecluster-nodegroup"
}
	
variable "endpoint_private_access" {
  type = bool
  default = true
  description = "Indicates whether or not the Amazon EKS private API server endpoint is enabled."
}

variable "endpoint_public_access" {
  type = bool
  default = true
  description = "Indicates whether or not the Amazon EKS public API server endpoint is enabled."
}


variable "ami_type" {
  description = "Defaults to AL2_x86_64. Valid values: AL2_x86_64, AL2_x86_64_GPU."
  type = string 
  default = "AL2_x86_64"
}

variable "disk_size" {
  description = "Disk size in GiB for worker nodes. Defaults to 20."
  type = number
  default = 20
}

variable "instance_types" {
  type = list(string)
  default = ["t3.medium"]
  description = "Set of instance types associated with the EKS Node Group."
}
