# ============================================================
# Terraform — AWS Infrastructure for DisasterWatch
# Provider: AWS (EKS + RDS MySQL + VPC)
# ============================================================

terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
}

# ── VPC ──────────────────────────────────────────────────────────────────────
resource "aws_vpc" "main" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_hostnames = true
  tags = { Name = "disasterwatch-vpc" }
}

resource "aws_subnet" "public" {
  count             = 2
  vpc_id            = aws_vpc.main.id
  cidr_block        = "10.0.${count.index}.0/24"
  availability_zone = data.aws_availability_zones.available.names[count.index]
  map_public_ip_on_launch = true
  tags = { Name = "disasterwatch-public-${count.index}" }
}

data "aws_availability_zones" "available" {}

# ── EKS Cluster (Kubernetes) ──────────────────────────────────────────────────
resource "aws_eks_cluster" "disasterwatch" {
  name     = "disasterwatch-cluster"
  role_arn = aws_iam_role.eks.arn

  vpc_config {
    subnet_ids = aws_subnet.public[*].id
  }

  tags = { Project = "DisasterWatch", Environment = var.environment }
}

resource "aws_iam_role" "eks" {
  name = "disasterwatch-eks-role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "eks.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "eks_policy" {
  policy_arn = "arn:aws:iam::aws:policy/AmazonEKSClusterPolicy"
  role       = aws_iam_role.eks.name
}

# ── RDS MySQL Database ────────────────────────────────────────────────────────
resource "aws_db_instance" "disaster_db" {
  identifier          = "disasterwatch-mysql"
  engine              = "mysql"
  engine_version      = "8.0"
  instance_class      = "db.t3.micro"
  allocated_storage   = 20
  db_name             = var.db_name
  username            = var.db_username
  password            = var.db_password
  skip_final_snapshot = true
  publicly_accessible = false
  vpc_security_group_ids = [aws_security_group.rds.id]

  tags = { Project = "DisasterWatch" }
}

resource "aws_security_group" "rds" {
  name   = "disasterwatch-rds-sg"
  vpc_id = aws_vpc.main.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.0.0.0/16"]
  }
}
