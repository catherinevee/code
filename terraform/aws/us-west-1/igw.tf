resource "aws_internet_gateway" "igw" {
  vpc_id = aws_vpc.eks-cluster-vpc.id

  tags = {
    Name = "main-ig-gateway"
  }
}