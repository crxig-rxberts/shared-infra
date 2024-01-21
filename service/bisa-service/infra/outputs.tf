output "ec2_public_ip" {
  value = aws_instance.bisa_service.public_ip
}