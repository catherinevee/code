module "fluentd_user" {
  source = "cloudposse/iam-system-user/aws"
  # Cloud Posse recommends pinning every module to a specific version
  # version     = "x.x.x"
  namespace = "eg"
  stage     = "dev"
  name      = "fluentd"

  policy_arns_map = {
    logs = "arn:aws:iam::aws:policy/CloudWatchLogsFullAccess"
  }

  inline_policies_map = {
    s3 = data.aws_iam_policy_document.s3_policy.json
  }
}

data "aws_iam_policy_document" "s3_policy" {
  statement {
    actions = [
      "s3:PutObject",
      "s3:GetObjectAcl",
      "s3:GetObject",
      "s3:ListBucket",
      "s3:PutObjectAcl"
    ]

    resources = [
      "arn:aws:s3:::bucket_name/*",
      "arn:aws:s3:::bucket_name/"
    ]
  }
}