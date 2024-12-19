variable "aws_profile" {
  description = "The AWS profile to use for deployment"
}

variable "public_subnet_cidrs" {
  description = "CIDR blocks for the public subnets"
  type        = list(string)
}

variable "availability_zones" {
  description = "Availability zones for the public subnets"
  type        = list(string)
}
# Database Configuration
variable "database_name" {
  description = "Name of the PostgreSQL database"
  type        = string
  default     = "assignment1_db"
}

variable "db_username" {
  description = "Master username for PostgreSQL"
  type        = string
  default     = "admin"
}

variable "db_password" {
  description = "Master password for PostgreSQL"
  type        = string
  default     = "StrongPassword123!"
}

variable "db_port" {
  description = "PostgreSQL port"
  type        = number
  default     = 5432
}

variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "vpc_cidr" {
  description = "CIDR block for the VPC"
  type        = string
}

variable "private_subnet_cidrs" {
  description = "CIDR blocks for the private subnets"
  type        = list(string)

}
# variable "public_subnet_cidrs" {
#   description = "CIDR blocks for the public subnets"
#   type        = list(string)
# }
variable "s3_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "assignment1-s3-bucket"
}
