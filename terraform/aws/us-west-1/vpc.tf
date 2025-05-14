resource "aws_vpc" "eks-cluster-vpc" {
  cidr_block = var.defaultvpc
}