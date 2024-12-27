provider "aws" {
  region  = var.region
  profile = var.aws_profile
}

# VPC
resource "aws_vpc" "vpc-01" {
  cidr_block           = var.vpc_cidr
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = {
    Name = "vpc-01"
  }
}

# Internet Gateway
resource "aws_internet_gateway" "ig-01" {
  vpc_id = aws_vpc.vpc-01.id
  tags = {
    Name = "ig-01"
  }
}

# Public Subnets in 3 Availability Zones 
resource "aws_subnet" "public_subnets" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.vpc-01.id
  cidr_block              = element(var.public_subnet_cidrs, count.index)
  availability_zone       = element(var.availability_zones, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}


# Private Subnets in 3 Availability Zones
resource "aws_subnet" "private_subnets" {
  count                   = length(var.private_subnet_cidrs)
  vpc_id                  = aws_vpc.vpc-01.id
  cidr_block              = element(var.private_subnet_cidrs, count.index)
  availability_zone       = element(var.availability_zones, count.index)
  map_public_ip_on_launch = false
  tags = {
    Name = "private-subnet-${count.index + 1}"
  }
}

# Public Route Table
resource "aws_route_table" "public_route_table" {
  vpc_id = aws_vpc.vpc-01.id
  tags = {
    Name = "public-route-table"
  }
}

# Private Route Table
resource "aws_route_table" "private_route_table" {
  vpc_id = aws_vpc.vpc-01.id
  tags = {
    Name = "private-route-table"
  }
}

# A route in the Public Route Table that sends traffic to the Internet Gateway
resource "aws_route" "public_route" {
  route_table_id         = aws_route_table.public_route_table.id
  destination_cidr_block = "0.0.0.0/0"
  gateway_id             = aws_internet_gateway.ig-01.id
}



# Associate Public Subnets with Public Route Table
resource "aws_route_table_association" "public_associations" {
  count          = length(var.public_subnet_cidrs)
  subnet_id      = aws_subnet.public_subnets[count.index].id
  route_table_id = aws_route_table.public_route_table.id
}


# Security Group for DB 
resource "aws_security_group" "database-security-group" {
  vpc_id = aws_vpc.vpc-01.id

  ingress {
    description = "Allow PostgreSQL from Mac Public IP"
    from_port   = 5432
    to_port     = 5432
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
  tags = {
    Name = "database-security-group"
  }
}

# Parameter Group for DB
resource "aws_db_parameter_group" "postgresql_parameter_group" {
  name        = "damg7245-postgresql-params"
  family      = "postgres16"
  description = "DB Parameter Group for webapp"

  parameter {
    name  = "rds.force_ssl"
    value = "0"
  }

  tags = {
    Name = "damg7245-postgresql-params"
  }
}

# DB Subnet Group (use private subnets)
resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "damg7245-db-subnet-group"
  subnet_ids = aws_subnet.public_subnets[*].id # Using private subnets for RDS instance

  tags = {
    Name = "damg7245-db-subnet-group"
  }
}

# RDS Instance
resource "aws_db_instance" "rds_instance" {
  allocated_storage      = 20
  instance_class         = "db.t4g.micro"
  engine                 = "postgres"
  engine_version         = "16.1"
  identifier             = "damg7245"
  db_name                = var.database_name
  username               = var.db_username
  password               = var.db_password
  parameter_group_name   = aws_db_parameter_group.postgresql_parameter_group.name
  skip_final_snapshot    = true
  publicly_accessible    = true
  vpc_security_group_ids = [aws_security_group.database-security-group.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name # Using DB Subnet Group
  multi_az               = false
  storage_encrypted      = true

  tags = {
    Name = "damg7245"
  }
}

resource "aws_iam_policy" "s3_bucket_policy" {
  name        = "S3BucketAccessPolicy"
  description = "Policy to allow access to S3 bucket"

  policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect = "Allow",
        Action = [
          "s3:ListBucket",
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ],
        Resource = [
          "arn:aws:s3:::${aws_s3_bucket.bucket.id}",
          "arn:aws:s3:::${aws_s3_bucket.bucket.id}/*"
        ]
      }
    ]
  })
} // IAM policy for S3 bucket

resource "aws_iam_role" "s3_access_role" {
  name = "S3AccessRole"
  assume_role_policy = jsonencode({
    Version = "2012-10-17",
    Statement = [
      {
        Effect    = "Allow",
        Principal = { Service = "ec2.amazonaws.com" },
        Action    = "sts:AssumeRole"
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "s3_policy_attachment" {
  role       = aws_iam_role.s3_access_role.name
  policy_arn = aws_iam_policy.s3_bucket_policy.arn
} // creating IAM Role and attaching the policy

resource "aws_s3_bucket" "bucket" {
  bucket        = var.s3_bucket_name
  force_destroy = true
}

resource "aws_s3_bucket_ownership_controls" "bucket" {
  bucket = aws_s3_bucket.bucket.id
  rule {
    object_ownership = "BucketOwnerPreferred"
  }
}

resource "aws_s3_bucket_acl" "bucket" {
  depends_on = [aws_s3_bucket_ownership_controls.bucket]

  bucket = aws_s3_bucket.bucket.id
  acl    = "private"
}

resource "aws_s3_bucket_lifecycle_configuration" "lifecycle_rule" {
  bucket = aws_s3_bucket.bucket.id

  rule {
    id     = "TransitionToStandardIA"
    status = "Enabled"

    transition {
      days          = 30
      storage_class = "STANDARD_IA"
    }
  }
}
