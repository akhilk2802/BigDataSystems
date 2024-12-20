# VPC Information
output "vpc_id" {
  value       = aws_vpc.vpc-01.id
  description = "The ID of the created VPC"
}

output "vpc_cidr_block" {
  value       = aws_vpc.vpc-01.cidr_block
  description = "The CIDR block of the created VPC"
}

# Subnets
output "public_subnet_ids" {
  value       = aws_subnet.public_subnets[*].id
  description = "List of Public Subnet IDs"
}

output "public_subnet_cidrs" {
  value       = aws_subnet.public_subnets[*].cidr_block
  description = "List of Public Subnet CIDR Blocks"
}

# Internet Gateway
output "internet_gateway_id" {
  value       = aws_internet_gateway.ig-01.id
  description = "The ID of the Internet Gateway"
}

# Route Tables
output "public_route_table_id" {
  value       = aws_route_table.public_route_table.id
  description = "The ID of the Public Route Table"
}

# Security Groups
output "database_security_group_id" {
  value       = aws_security_group.database-security-group.id
  description = "The ID of the Security Group for the PostgreSQL Database"
}

# RDS Instance
output "rds_instance_id" {
  value       = aws_db_instance.rds_instance.id
  description = "The ID of the RDS PostgreSQL instance"
}

output "rds_instance_endpoint" {
  value       = aws_db_instance.rds_instance.endpoint
  description = "The endpoint for connecting to the RDS PostgreSQL instance"
}

output "rds_instance_db_name" {
  value       = aws_db_instance.rds_instance.db_name
  description = "The name of the RDS database"
}

# S3 Bucket Details
output "s3_bucket_id" {
  value       = aws_s3_bucket.bucket.id
  description = "The name of the created S3 bucket"
}

output "s3_bucket_arn" {
  value       = aws_s3_bucket.bucket.arn
  description = "The ARN of the created S3 bucket"
}

output "s3_bucket_policy_arn" {
  value       = aws_iam_policy.s3_bucket_policy.arn
  description = "The ARN of the IAM Policy attached to the S3 bucket"
}

output "s3_access_role_name" {
  value       = aws_iam_role.s3_access_role.name
  description = "The IAM Role Name for S3 Access"
}

# IAM Role and Policy
output "s3_access_role_arn" {
  value       = aws_iam_role.s3_access_role.arn
  description = "The ARN of the IAM Role for S3 Access"
}

output "s3_access_policy_attachment_id" {
  value       = aws_iam_role_policy_attachment.s3_policy_attachment.id
  description = "The ID of the IAM Role Policy Attachment"
}