resource "aws_subnet" "private-az0" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = var.default_privatesubnets[0]
  availability_zone = var.defaultaz[0]

  tags = {
    Name = "private_${var.defaultaz[0]}"
    "kubernetes.io/role/internal-elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}


resource "aws_subnet" "public-az1" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = var.default_publicsubnets[0]
  availability_zone = var.defaultaz[1]

  tags = {
    Name = "public_${var.defaultaz[1]}"
    "kubernetes.io/role/elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}
resource "aws_subnet" "public-az0" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = var.default_publicsubnets[1]
  availability_zone = var.defaultaz[0]

  tags = {
    Name = "public_${var.defaultaz[0]}"
    "kubernetes.io/role/elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}
resource "aws_subnet" "private-az1" {
  vpc_id     = aws_vpc.eks-cluster-vpc.id
  cidr_block = var.default_privatesubnets[1]
  availability_zone = var.defaultaz[1]

  tags = {
    Name = "private_${var.defaultaz[1]}"
    "kubernetes.io/role/internal-elb" = 1
    "kubernetes.io/cluster/eks-cluster-production" = "shared"
  }
}