variable "instance_tags" {
  description = "Tags for EC2 instance"
  type        = map(string)

  validation {
    condition = alltrue([
      for required_tag in ["project", "environment", "team", "cost_center", "owner"] :
      contains(keys(var.instance_tags), required_tag)
    ])
    error_message = "All instances must include required tags: project, environment, team, cost_center, owner."
  }
}