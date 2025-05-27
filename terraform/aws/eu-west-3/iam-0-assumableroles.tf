module "iam_assumable_roles" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-assumable-roles"

  trusted_role_arns = [
    "arn:aws:iam::025066254478:user/qatherine",
    "arn:aws:iam::025066254478:user/catherine",
    "arn:aws:iam::025066254478:user/katherine",

  ]

  create_admin_role = true

  create_poweruser_role = true
  poweruser_role_name   = "developer"

  create_readonly_role       = true
  readonly_role_requires_mfa = false
}