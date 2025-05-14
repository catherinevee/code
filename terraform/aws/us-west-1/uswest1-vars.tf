
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