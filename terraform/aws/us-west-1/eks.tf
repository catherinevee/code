resource "aws_eks_cluster" "prod-eks-cluster" {
  name     = var.default_eks
  role_arn = aws_iam_role.eks-role.arn

  vpc_config {
    security_group_ids      = [
      aws_security_group.eks_cluster.id,
       aws_security_group.eks_nodes.id
       ]
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