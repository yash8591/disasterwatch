output "eks_cluster_name" {
  description = "Name of the EKS cluster"
  value       = aws_eks_cluster.disasterwatch.name
}

output "rds_endpoint" {
  description = "MySQL RDS endpoint — use as DB_HOST in backend .env"
  value       = aws_db_instance.disaster_db.endpoint
  sensitive   = true
}

output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}
