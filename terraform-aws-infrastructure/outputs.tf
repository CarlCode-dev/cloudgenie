output "web_public_ip" {
  value = aws_eip.web_eip.public_ip
}

output "vpc_id" {
  description = "ID of the created VPC"
  value       = aws_vpc.main.id
}