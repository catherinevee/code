module "iam_account" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-account"

  account_alias = "catherinecompany"

  minimum_password_length = 37
  require_numbers         = false
}

module "iam_assumable_roles" {
  source = "../../modules/iam-assumable-roles"

  trusted_role_arns = [
    "arn:aws:iam::307990089504:root",
    "arn:aws:iam::835367859851:user/anton",
  ]

  trusted_role_services = [
    "codedeploy.amazonaws.com"
  ]

  create_admin_role = true

  create_poweruser_role      = true
  poweruser_role_name        = "Billing-And-Support-Access"
  poweruser_role_policy_arns = ["arn:aws:iam::aws:policy/job-function/Billing", "arn:aws:iam::aws:policy/AWSSupportAccess"]

  create_readonly_role       = true
  readonly_role_requires_mfa = false
}


module "iam_assumable_roles_in_prod" {
  source = "../../modules/iam-assumable-roles"

  trusted_role_arns = [
    "arn:aws:iam::${data.aws_caller_identity.iam.account_id}:root",
  ]

  create_admin_role     = true
  create_poweruser_role = true

  create_readonly_role       = true
  readonly_role_requires_mfa = false

  providers = {
    aws = aws.production
  }
}
