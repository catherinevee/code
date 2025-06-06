
variable "defaultregion" {
    type = string
    default = "us-east-1"
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
      "use1-az1",
      "use1-az2",
      "use1-az3"
    ]
}

variable "defaultenv" {
    type = string
    default = "prod"
}

variable "defaultvpc" {
    type = string
    default = "10.40.0.0/16"
}

variable "default_privatesubnets" {
    type = list(string)
    default = [
      "10.40.1.0/24",
      "10.40.2.0/24",
      "10.40.3.0/24",
    ]
}

variable "default_publicsubnets" {
    type = list(string)
    default = [
      "10.40.10.0/24",
      "10.40.20.0/24",
      "10.40.30.0/24",
    ]
}

#===================
variable "default_eks" {
  type = string
  default = "eks-catherinecluster"
}