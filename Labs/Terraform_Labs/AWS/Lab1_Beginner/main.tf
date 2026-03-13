provider "aws" {
  region = "us-west-2"
}

# S3 bucket for storing ML model artifacts
resource "aws_s3_bucket" "ml_artifacts" {
  bucket = "mlops-model-artifacts-harini"

  tags = {
    Name        = "MLOps Model Artifacts"
    Environment = "Dev"
    Project     = "MLOps Lab"
  }
}

# VPC for isolating ML workloads
resource "aws_vpc" "ml_vpc" {
  cidr_block = "10.1.0.0/16"

  tags = {
    Name = "mlops-vpc"
  }
}

# Subnet within the VPC
resource "aws_subnet" "ml_subnet" {
  vpc_id     = aws_vpc.ml_vpc.id
  cidr_block = "10.1.1.0/24"

  tags = {
    Name = "mlops-subnet"
  }
}

# Enable versioning for ML model version tracking
resource "aws_s3_bucket_versioning" "ml_artifacts_versioning" {
  bucket = aws_s3_bucket.ml_artifacts.id

  versioning_configuration {
    status = "Enabled"
  }
}