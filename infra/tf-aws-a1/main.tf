provider "aws" {
  region  = var.aws_region
  profile = var.aws_profile
}

# VPC and Security Groups
resource "aws_vpc" "main" {
  cidr_block = "10.0.0.0/16"
}

resource "aws_subnet" "main" {
  count                   = length(var.public_subnet_cidrs)
  vpc_id                  = aws_vpc.main.id
  cidr_block              = element(var.public_subnet_cidrs, count.index)
  availability_zone       = element(var.availability_zones, count.index)
  map_public_ip_on_launch = true
  tags = {
    Name = "public-subnet-${count.index + 1}"
  }
}

resource "aws_security_group" "rds_sg" {
  name        = "rds_security_group"
  description = "Allow access to RDS instance"
  vpc_id      = aws_vpc.main.id

  ingress {
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
}

resource "aws_db_subnet_group" "db_subnet_group" {
  name       = "damg7245-db-subnet-group"
  subnet_ids = aws_subnet.main[*].id
  tags = {
    Name = "csye6225-db-subnet-group"
  }
}

# Create an RDS PostgreSQL Instance
resource "aws_db_instance" "rds_instance" {
  allocated_storage      = 20
  instance_class         = "db.t4g.micro"
  engine                 = "postgres"
  engine_version         = "16.1"
  identifier             = "damg7245"
  db_name                = var.database_name
  username               = var.db_username
  password               = var.db_password
  skip_final_snapshot    = true
  publicly_accessible    = false
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.db_subnet_group.name
  multi_az               = false

  tags = {
    Name = "csye6225"
  }
}

