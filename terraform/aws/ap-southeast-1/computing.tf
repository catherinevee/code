# Create an EC2 instance
resource "aws_instance" "poland-ec2-cath-1" {
  ami           = "ami-785db401"
  instance_type = "t2.micro"
  
}