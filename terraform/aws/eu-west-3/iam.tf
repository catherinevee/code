module "iam_account" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-account"

  account_alias = "catherinecompany"

  minimum_password_length = 37
  require_numbers         = false
}
