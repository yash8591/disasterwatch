output "vpc_id" {
  description = "VPC ID"
  value       = aws_vpc.main.id
}

output "eks_cluster_name" {
  description = "Name of the EKS cluster"
  value       = aws_eks_cluster.disasterwatch.name
}

output "rds_endpoint" {
  description = "MySQL RDS endpoint — use as DB_HOST in backend deployment"
  value       = aws_db_instance.disaster_db.endpoint
}

output "frontend_ecr_url" {
  description = "URL of the Frontend ECR repository"
  value       = aws_ecr_repository.frontend.repository_url
}

output "backend_ecr_url" {
  description = "URL of the Backend ECR repository"
  value       = aws_ecr_repository.backend.repository_url
}
