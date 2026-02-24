output "ec2_public_ip" {
  description = "InfraGuard EC2 public IP"
  value       = aws_instance.infraguard.public_ip
}

output "ec2_public_dns" {
  description = "InfraGuard EC2 public DNS"
  value       = aws_instance.infraguard.public_dns
}

output "dashboard_url" {
  description = "InfraGuard dashboard URL"
  value       = "http://${aws_instance.infraguard.public_ip}:8080"
}

output "grafana_url" {
  description = "Grafana dashboard URL"
  value       = "http://${aws_instance.infraguard.public_ip}:3000"
}

output "ssh_command" {
  description = "SSH command to connect"
  value       = "ssh -i ~/.ssh/infraguard-key.pem ubuntu@${aws_instance.infraguard.public_ip}"
}
