module "iam_policy_from_data_source" {
  source = "../../modules/iam-policy"
  name        = "EC2 Policy"
  path        = "/"
  description = "Policy to limit EC2 access"
  policy = data.aws_iam_policy_document.ec2_policy.json
  
}