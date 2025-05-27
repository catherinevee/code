
#creating users (for human identities)
#the name of the module is the name of the user
module "catherine" {
  source = "cloudposse/iam-user/aws"
  version     = "1.2.1"
  name       = "catherine"
  user_name  = "catherine@outlook.com"
  pgp_key    = "keybase:catherine"
  groups     = ["admins"]
}


#creating users (for human identities)
#the name of the module is the name of the user
module "qatherine" {
  source = "cloudposse/iam-user/aws"
  version     = "1.2.1"
  name       = "qatherine"
  user_name  = "qatherine@outlook.com"
  pgp_key    = "keybase:qatherine"
  groups     = ["admins"]
}

module "katherine" {
  source = "cloudposse/iam-user/aws"
  version     = "1.2.1"
  name       = "katherine"
  user_name  = "katherine@outlook.com"
  pgp_key    = "keybase:katherine"
  groups     = ["admins"]
}


module "kathryn" {
  source = "cloudposse/iam-user/aws"
  version     = "1.2.1"
  name       = "kathryn"
  user_name  = "kathryn@outlook.com"
  pgp_key    = "keybase:kathryn"
}

module "catharine" {
  source = "cloudposse/iam-user/aws"
  version     = "1.2.1"
  name       = "catharine"
  user_name  = "catharine@outlook.com"
  pgp_key    = "keybase:catharine"
}



