
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



############################

variable "peer_defaulttags" {
  description = "Common tags for all resources"
  type = object({
    Environment = string
    OU   = string
  })
  default = {
    Environment = "prod"
    OU   = "EnterpriseApplications"
  }
}



variable "peer_defaultregion" {
    type = string
    default = "us-west-1"
}

variable "peer_defaultaz" {
    type = list(string)
    default = [
      "usw1-az1",
      "usw1-az2",
      "usw1-az3"
    ]
}

variable "peer_defaultvpc" {
    type = string
    default = "defaultvpc_peer"
}

variable "peer_defaultcidr" {
    type = string
    default = "10.5.0.0/16"
}

variable "peer_defaultprivatesubnets" {
    type = list(string)
    default = [
      "10.5.1.0/24",
      "10.5.2.0/24",
      "10.5.3.0/24",
    ]
}