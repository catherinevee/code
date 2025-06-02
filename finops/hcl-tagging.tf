locals {
  common_tags = {
    Project     = var.project_name
    Environment = var.environment
    Team        = var.team_name
    Owner       = var.owner_email
    CostCenter  = var.cost_center
    ManagedBy   = "terraform"
    CreatedDate = formatdate("YYYY-MM-DD", timestamp())
  }
}

resource "aws_instance" "web" {
  ami           = var.ami_id
  instance_type = var.instance_type

  tags = merge(local.common_tags, {
    Name        = "${var.project_name}-web-${var.environment}"
    Component   = "web-server"
    Billable    = "true"
  })
}

resource "aws_s3_bucket" "assets" {
  bucket = "${var.project_name}-assets-${var.environment}"

  tags = merge(local.common_tags, {
    Component = "static-assets"
    Backup    = "daily"
  })
}