resource "aws_eks_node_group" "prod-eks-node-group" {
  cluster_name    = aws_eks_cluster.prod-eks-cluster.name
  node_group_name = "prod-group"
  node_role_arn   = aws_iam_role.eks-role.arn
  subnet_ids      = [
        aws_subnet.private-az1.id,
        aws_subnet.private-az0.id,
    ]

  scaling_config {
    desired_size = 3
    max_size     = 4
    min_size     = 1
  }

  update_config {
    max_unavailable = 1
  }

  capacity_type = "ON_DEMAND"
  instance_types = ["t3.micro"]
  depends_on = [
    aws_iam_role_policy_attachment.eks-ng-AmazonEKSWorkerNodePolicy,
    aws_iam_role_policy_attachment.eks-ng-AmazonEKS_CNI_Policy,
    aws_iam_role_policy_attachment.eks-ng-AmazonEC2ContainerRegistryReadOnly,
  ]
}