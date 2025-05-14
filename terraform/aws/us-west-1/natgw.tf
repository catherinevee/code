resource "aws_eip" "nat" {
  count = 1
}



resource "aws_nat_gateway" "public-az1-natgw" {
  allocation_id = aws_eip.nat-ip.id
  subnet_id     = aws_subnet.public-az1.id

  tags = {
    Name = "gw NAT"
  }

  depends_on = [aws_internet_gateway.igw]
}