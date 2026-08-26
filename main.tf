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


import {
  to = aws_ecr_repository.flaskapp
  id = "prod-flask-app-image" 
}


# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "prod-flask-app-image"
resource "aws_ecr_repository" "flaskapp" {
  force_delete         = null
  image_tag_mutability = "MUTABLE"
  name                 = "prod-flask-app-image"
  region               = "eu-north-1"
  tags                 = {}
  tags_all             = {}
  encryption_configuration {
    encryption_type = "KMS"
    kms_key         = "arn:aws:kms:eu-north-1:140023390772:key/66463763-1109-4926-923e-cc2b85718c64"
  }
  image_scanning_configuration {
    scan_on_push = true
  }
}


import {
  to = aws_ecs_cluster.host
  id = "prod-flask-app-image-cluster"   
}

import {
  to = aws_ecs_task_definition.config
  id = "arn:aws:ecs:eu-north-1:140023390772:task-definition/prod-flask-app-image-task-definition:2"  #
}

import {
  to = aws_s3_bucket.infra
  id = "my-photos-albums-123"          # your own s3 bucket name
}


# __generated__ by Terraform
# Please review these resources and move them into your main configuration files.

# __generated__ by Terraform from "prod-flask-app-image-cluster"
resource "aws_ecs_cluster" "host" {
  name     = "prod-flask-app-image-cluster"
  region   = "eu-north-1"
  tags     = {}
  tags_all = {}
  configuration {
    execute_command_configuration {
      kms_key_id = null
      logging    = "DEFAULT"
    }
  }
  setting {
    name  = "containerInsights"
    value = "disabled"
  }
}

# __generated__ by Terraform from "arn:aws:ecs:eu-north-1:140023390772:task-definition/prod-flask-app-image-task-definition:2"
resource "aws_ecs_task_definition" "config" {
  container_definitions = jsonencode([{
    environment = []
    environmentFiles = [{
      type  = "s3"
      value = "arn:aws:s3:::my-photos-albums-123/env/25)_environment_variables.env"
    }]
    essential = true
    image     = "140023390772.dkr.ecr.eu-north-1.amazonaws.com/prod-flask-app-image@sha256:7a782f7516cd22b1afa5e95831174dfac8e7b64ecb9eed6c1882129bd672ece5"
    logConfiguration = {
      logDriver = "awslogs"
      options = {
        awslogs-create-group  = "true"
        awslogs-group         = "/ecs/prod-flask-app-image-task-definition"
        awslogs-region        = "eu-north-1"
        awslogs-stream-prefix = "ecs"
      }
      secretOptions = []
    }
    mountPoints = []
    name        = "flask-app-container"
    portMappings = [{
      appProtocol   = "http"
      containerPort = 80
      hostPort      = 80
      name          = "flask-app-container-80-tcp"
      protocol      = "tcp"
      }, {
      appProtocol   = "http"
      containerPort = 443
      hostPort      = 443
      name          = "flask-app-container-443-tcp"
      protocol      = "tcp"
    }]
    systemControls = []
    ulimits        = []
    volumesFrom    = []
  }])
  cpu                      = "1024"
  enable_fault_injection   = false
  execution_role_arn       = "arn:aws:iam::140023390772:role/ecsTaskExecutionRole"
  family                   = "prod-flask-app-image-task-definition"
  ipc_mode                 = null
  memory                   = "2048"
  network_mode             = "awsvpc"
  pid_mode                 = null
  region                   = "eu-north-1"
  requires_compatibilities = ["FARGATE"]
  skip_destroy             = null
  tags                     = {}
  tags_all                 = {}
  task_role_arn            = null
  track_latest             = false
  runtime_platform {
    cpu_architecture        = "X86_64"
    operating_system_family = "LINUX"
  }
}

# __generated__ by Terraform from "my-photos-albums-123"
resource "aws_s3_bucket" "infra" {
  bucket              = "my-photos-albums-123"
  bucket_namespace    = "global"
  force_destroy       = false
  object_lock_enabled = false
  region              = "eu-north-1"
  tags                = {}
  tags_all            = {}
}

