resource "aws_security_group" "web" {
  name        = "web-security-group"
  description = "Security group for web servers"

  dynamic "ingress" {
    for_each = var.security_rules.allow_http ? [1] : []
    content {
      from_port   = 80
      to_port     = 80
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTP access"
    }
  }

  dynamic "ingress" {
    for_each = var.security_rules.allow_https ? [1] : []
    content {
      from_port   = 443
      to_port     = 443
      protocol    = "tcp"
      cidr_blocks = ["0.0.0.0/0"]
      description = "HTTPS access"
    }
  }

  dynamic "ingress" {
    for_each = var.security_rules.allow_ssh ? [1] : []
    content {
      from_port   = 22
      to_port     = 22
      protocol    = "tcp"
      cidr_blocks = var.security_rules.ssh_cidrs
      description = "SSH access"
    }
  }
}