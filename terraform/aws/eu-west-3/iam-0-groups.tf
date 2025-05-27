module "iam_group_with_assumable_roles_policy" {
  source  = "terraform-aws-modules/iam/aws//modules/iam-group-with-assumable-roles-policy"

  name = "production-readonly"

  assumable_roles = [
    "arn:aws:iam::025066254478:role/readonly"  # these roles can be created using `iam_assumable_roles` submodule
  ]

  group_users = [
    "catharine",
    "kathryn"
  ]
}
