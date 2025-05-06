

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
      "apsoutheast-1"
    ]
}

variable "defaultenv" {
    type = string
    default = "prod"
}

variable "defaultvpc" {
    type = string
    default = "defaultvpc"
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
      "10.101.1.0/24",
      "10.101.2.0/24",
      "10.101.3.0/24",
    ]
}

variable "defaultcidr" {
    type = string
    default = "10.0.0.0/16"
}

