#===============================================
#these variable values are filled in at runtime
#in the tfvars files
#===============================================
variable "app_config" {
  description = "Application configuration"
  type = object({
    name         = string
    environment  = string
    domain       = string
    features = object({
      https_redirect    = bool
      waf_protection   = bool
      auto_scaling     = bool
      database_backup  = bool
      monitoring       = bool
    })
    scaling = object({
      min_instances = number
      max_instances = number
      target_cpu    = number
    })
  })
}


variable "workstations" {
  description = "Deployed EC2 Instances, dependant on environment"
  type = map(object({
    instance_type = string
    enable_https  = bool
    backup_days   = number
  }))
  default = {}
}

variable "security_rules" {
  description = "Security rules configuration"
  type = object({
    allow_http    = bool
    allow_https   = bool
    allow_ssh     = bool
    ssh_cidrs     = list(string)
  })
}

variable "features" {
  description = "Feature flags for optional components"
  type = object({
    monitoring    = bool
    auto_scaling  = bool
    cdn          = bool
    cache        = bool
  })
  default = {
    monitoring   = false
    auto_scaling = false
    cdn         = false
    cache       = false
  }
}
#===============================================
#end above
#===============================================

variable "defaulttags" {
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

variable "environment" {
    type = string
    default = "dev"
}


variable "defaultlocation" {
    type = string
    default = "ap-northeast-1"
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

