# AWS Config Rule to detect untagged resources
resource "aws_config_configuration_recorder" "main" {
  name     = "cost-compliance-recorder"
  role_arn = aws_iam_role.config.arn

  recording_group {
    all_supported = true
  }
}

resource "aws_config_config_rule" "required_tags" {
  name = "required-tags-compliance"

  source {
    owner             = "AWS"
    source_identifier = "REQUIRED_TAGS"
  }

  input_parameters = jsonencode({
    tag1Key   = "project"
    tag2Key   = "environment"
    tag3Key   = "team"
    tag4Key   = "cost_center"
    tag5Key   = "owner"
  })

  depends_on = [aws_config_configuration_recorder.main]
}