variable "tags" {
  description = "Common tags for all resources"
  type = object({
    Environment = string
    OU   = string
  })
  default = {
    Environment = "dev"
    OU   = "IT"
  }
}

variable "defaultenv" {
    type = string
    default = "dev"
}


variable "defaultemail" {
    type = string
    default = "catherine.vee@outlook.com"
}

variable "defaultname" {
    type = string
    default = "Catherine Vee"
}


variable "defaultrg" {
 type = string
 default = "mexicocentralrg-dev" 
}
variable "defaultlocation" {
 type = string
 default = "mexicocentral" 
}

variable "mexicocentralresourcegroups" {
    type = list(string)
    default = [
         "mexicocentralrg-prod",
         "mexicocentralrg-test",
         "mexicocentralrg-dev"
        ]
}

variable "defaultacr" {
 type = string
 default = "mexicocentralacr" 
}
