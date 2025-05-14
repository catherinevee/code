resource "aws_eks_cluster" "prod-eks-cluster" {
  name     = var.default_eks
  role_arn = aws_iam_role.eks-role.arn

  vpc_config {
    subnet_ids = [
        aws_subnet.private-az1.id,
        aws_subnet.public-az0.id,
        aws_subnet.private-az0.id,
        aws_subnet.public-az1.id
        ]
  }

  depends_on = [
    aws_iam_role_policy_attachment.eks-AmazonEKSClusterPolicy
  ]
}