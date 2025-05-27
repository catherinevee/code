
module "iam_policy_from_data_source" {
  source = "../../modules/iam-policy"

  name        = "CUSTOM-POLICY-EC2"
  path        = "/"
  description = "Custom EC2 Policy"

  policy = data.aws_iam_policy_document.ec2_policy.json

  
}


module "iam_policy_from_data_source" {
  source = "../../modules/iam-policy"

  name        = "CUSTOM-POLICY-VPC"
  path        = "/"
  description = "Custom VPC Policy"

  policy = data.aws_iam_policy_document.vpc_policy.json

}

module "iam_policy_from_data_source" {
  source = "../../modules/iam-policy"

  name        = "CUSTOM-POLICY-DYNAMODB"
  path        = "/"
  description = "Custom DynamoDB Policy"

  policy = data.aws_iam_policy_document.dynamodb_policy.json

}