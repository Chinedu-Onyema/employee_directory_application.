provider "aws" {
    region = "eu-north-1"               # set to your region at aws configure
}

# -----------------------------------------------------
# RDS SECURITY GROUP RESOURCE: Controls who can access the database
# Attach this resource group to your RDS instance resource
# -----------------------------------------------------
resource "aws_security_group" "rds_sg" {
  name = "rds-security-group"
  description = "Allow MySQL inbound and outbound traffic"

  ingress {
    description = "MySQL port"
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]          # restrict this to your IP in production
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"                   # RDS database connect to all protocols (TCP, UDP, ICMP, everything)
    cidr_blocks = ["0.0.0.0/0"]
  }

    tags = {
    Name        = "RDS_SG"
  }
}


# -------------------------------------------------------------
# RDS SUBNET GROUP RESOURCE: Defines which subnets RDS can use
# Attach this resource group to your RDS instance resource
# -------------------------------------------------------------

resource "aws_db_subnet_group" "rds_subnet_group" {
  name       = "rds-subnet-group"
  subnet_ids = ["subnet-034183c35c27efbd3", "subnet-039184029a381ce19"]       # use your own public subnet ids
}


# -----------------------------------------------------
# RDS MYSQL INSTANCE RESOURCE
# -----------------------------------------------------

resource "aws_db_instance" "mysql_db" {
  engine         = "mysql"
  engine_version = "8.4.8"
  instance_class = "db.t3.micro"
  allocated_storage     = 20
  storage_type          = "gp2"
  db_name  = "employees"                         # use the exact name stated in database_create_tables.sql
  username = "admin"
  password = "YourStrongPassword123!"
  publicly_accessible = true                      # make sure you set this to true      
  multi_az = false
  skip_final_snapshot = true
  db_subnet_group_name   = aws_db_subnet_group.rds_subnet_group.name          # Attach your subnet group name
  vpc_security_group_ids = [aws_security_group.rds_sg.id]                     # Attach your security group id. [] means multiple SGs

  lifecycle {
    prevent_destroy = false                                                   # delete database enabled on terraform destroy
  }

  tags = {
    Name        = "flaskapp-database"
  }
}


# ------------------------------------------------------
# THIS SHOWS THE OUTPUT VALUES YOU WILL 
# NEED FOR YOUR DATABASE CONNECTION
# ------------------------------------------------------

output "rds_endpoint" {
  description = "The connection endpoint of the RDS instance"
  value       = aws_db_instance.mysql_db.address
}

output "rds_db_user" {
  description = "The user of the RDS instance"
  value       = aws_db_instance.mysql_db.username
}

output "rds_db_name" {
  description = "The name of the database"
  value       = aws_db_instance.mysql_db.db_name
}

output "rds_db_password" {
  description = "The ID of the RDS instance"
  value       = aws_db_instance.mysql_db.password
  sensitive   = true
}


resource "aws_dynamodb_table" "employees" {
    name = "Employees"
    billing_mode = "PAY_PER_REQUEST"
    hash_key = "id"
    
    attribute {
        name = "id"
        type = "S"
    }
}
