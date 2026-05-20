variable "aws_region" {
  description = "AWS region to deploy resources"
  default     = "ap-south-1"   # Mumbai (closest to India)
}

variable "environment" {
  description = "Deployment environment"
  default     = "production"
}

variable "db_name" {
  description = "MySQL database name"
  default     = "disaster_db"
}

variable "db_username" {
  description = "MySQL master username"
  default     = "admin"
}

variable "db_password" {
  description = "MySQL master password"
  sensitive   = true
  # Set via: export TF_VAR_db_password="your_password"
}
