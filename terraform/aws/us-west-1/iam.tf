#===================================
#permissions for the EKS cluster
data "aws_iam_policy_document" "assume_role" {
  statement {
    effect = "Allow"
    principals {
      type        = "Service"
      identifiers = ["eks.amazonaws.com"]
    }

    actions = ["sts:AssumeRole"]
  }
}

resource "aws_iam_role" "eks-role" {
  name               = "eks-cluster-role"
  assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

resource "aws_iam_role_policy_attachment" "eks-AmazonEKSClusterPolicy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks-role.name
}

#permissions for the node groups inside of the EKS cluster

resource "aws_iam_role" "eks-nodegroup" {
  name = var.default_eks-nodegroup

  assume_role_policy = jsonencode({
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Principal = {
        Service = "ec2.amazonaws.com"
      }
    }]
    Version = "2012-10-17"
  })
}

resource "aws_iam_role_policy_attachment" "eks-ng-AmazonEKSWorkerNodePolicy" {
# Allows them to connect to EKS clusters
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSWorkerNodePolicy"
  role       = aws_iam_role.eks-nodegroup.name
}

resource "aws_iam_role_policy_attachment" "eks-ng-AmazonEKS_CNI_Policy" {
# Service that Adds IP addresses to kubernetes nodes
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKS_CNI_Policy"
  role       = aws_iam_role.eks-nodegroup.name
}

resource "aws_iam_role_policy_attachment" "eks-ng-AmazonEC2ContainerRegistryReadOnly" {
# ECR for images if exists
  policy_arn = "arn:aws:iam::aws:policy/AmazonEC2ContainerRegistryReadOnly"
  role       = aws_iam_role.eks-nodegroup.name
}

