# terraform/modules/common/variables.tf
variable "required_tags" {
  description = "Tags required for all resources - these enable cost attribution"
  type = object({
    project      = string  # Which business project or product
    environment  = string  # dev, staging, prod
    team         = string  # Who owns this resource
    cost_center  = string  # Where to allocate costs
    owner        = string  # Primary contact (email)
  })
}

variable "optional_tags" {
  description = "Additional tags that provide operational context"
  type = object({
    backup_schedule = string  # How frequently to backup
    monitoring      = string  # Monitoring level required
    compliance      = string  # Compliance requirements
    data_class      = string  # Data sensitivity level
  })
  default = {
    backup_schedule = "daily"
    monitoring      = "standard"
    compliance      = "internal"
    data_class      = "general"
  }
}
