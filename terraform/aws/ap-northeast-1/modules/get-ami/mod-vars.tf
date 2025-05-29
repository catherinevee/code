variable "ubuntu_version" {
  type        = string
  description = "Ubuntu version"
  default     = "24.04"
}

variable "arch" {
  type        = string
  description = "Processor architecture"
  default     = "amd64"
}

variable "virtualization_type" {
  type        = string
  description = "Virtualization type"
  default     = "hvm"
}

variable "volume_type" {
  type        = string
  description = "Volume type"
  default     = "ebs-gp3"
}