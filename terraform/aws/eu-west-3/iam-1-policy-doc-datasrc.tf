data "aws_iam_policy_document" "ec2_policy" {
  statement {
    sid       = "AllowDescribeEC2Instances"
    actions   = [
      "ec2:DescribeInstances",
      "ec2:DescribeVolumes",
      "ec2:DescribeImages"
    ]
    resources = ["*"]
  }

  statement {
    sid       = "AllowStartStopSpecificEC2Instance"
    actions   = [
      "ec2:StartInstances",
      "ec2:StopInstances"
    ]
    #resources = ["arn:aws:ec2:REGION:ACCOUNT_ID:instance/INSTANCE_ID"]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "lambda_policy" {
  statement {
    sid       = "AllowInvokeSpecificLambdaFunction"
    actions   = [
      "lambda:InvokeFunction"
    ]
    resources = ["*"]
  }

  statement {
    sid       = "AllowListLambdaFunctions"
    actions   = [
      "lambda:ListFunctions"
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "dynamodb_policy" {
  statement {
    sid       = "AllowReadWriteSpecificDynamoDBTable"
    actions   = [
      "dynamodb:GetItem",
      "dynamodb:PutItem",
      "dynamodb:UpdateItem",
      "dynamodb:DeleteItem"
    ]
    resources = ["*"]
  }

  statement {
    sid       = "AllowDescribeDynamoDBTable"
    actions   = [
      "dynamodb:DescribeTable"
    ]
    resources = ["*"]
  }
}

data "aws_iam_policy_document" "vpc_policy" {
  statement {
    sid       = "AllowDescribeVPCResources"
    actions   = [
      "ec2:DescribeVpcs",
      "ec2:DescribeSubnets",
      "ec2:DescribeSecurityGroups",
      "ec2:DescribeRouteTables",
      "ec2:DescribeNetworkAcls",
      "ec2:DescribeInternetGateways"
    ]
    resources = ["*"]
  }

  statement {
    sid       = "AllowCreateVPC"
    actions   = [
      "ec2:CreateVpc"
    ]
    resources = ["*"] # VPC creation typically applies to all regions/accounts
  }

  statement {
    sid       = "AllowModifySpecificVPC"
    actions   = [
      "ec2:ModifyVpcAttribute",
      "ec2:DeleteVpc"
    ]
    resources = ["*"]
  }
}