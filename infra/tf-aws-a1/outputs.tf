output "db_endpoint" {
  description = "PostgreSQL RDS endpoint"
  value       = aws_db_instance.rds_instance.endpoint
}

output "db_port" {
  description = "Database port"
  value       = aws_db_instance.rds_instance.port
}

output "db_name" {
  description = "Database name"
  value       = aws_db_instance.rds_instance.db_name
}

output "db_username" {
  description = "Database username"
  value       = aws_db_instance.rds_instance.username
}
