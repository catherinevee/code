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

variable "defaultlocation" {
    type = string
    default = "francecentral"
}

variable "defaultrg" {
    type = string
    default = "france-prod"
}


variable "defaultanalyticsworkspace" {
    type = string
    default = "france-analytics-workspace"
}
variable "polandcentral-var-prodresourcegroups" {
    type = list(string)
    default = [
         "francecentralrg-prod",
         "francecentralrg-test",
         "francecentralrg-dev"
        ]
}


variable "polandcentral-var-instances" {
    type = list(string)
    default = [
         "francec-production",
         "francec-test",
         "francec-dev"
        ]
}



variable "defaultenv" {
  type = string
  default = "prod"
}

variable "defaultaks_clustername" {
    type = string
    default = "cathy-prod-cluster"
}


variable "defaultaks_dnsname" {
    type = string
    default = "catherine89102nf"
}

variable "defaultacr" {
    type = string
    default = "catherineacr"
}


variable "defaultvnet" {
    type = string
    default = "10.0.0.0/16"
}



variable "defaultcontainerappenv" {
    type = string
    default = "containerappenv-default"
}

variable "defaultcontainerapp" {
    type = string
    default = "containerapp-default"
}

