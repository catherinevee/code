variable "tags" {
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
 default = "mexicocentral-dev" 
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
 default = "mexicocentral-acr" 
}
