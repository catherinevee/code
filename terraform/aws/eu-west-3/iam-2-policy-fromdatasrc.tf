
module "iam_policy_from_data_source" {
  source = "../../modules/iam-policy"

  name        = "CUSTOM-POLICY-EC2"
  path        = "/"
  description = "thing"

  policy = data.aws_iam_policy_document.ec2_policy.json

  
}