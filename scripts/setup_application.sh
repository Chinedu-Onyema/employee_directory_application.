#!/bin/bash

# exits the script immediately if any command fails (stops on errors)
set -e

echo "Setting up application..."

# Change to app directory we created instance our ec2 instance/
# where our application code is located/ 
# This is where we will install dependencies and run our app.
cd /var/www/employee-directory

# Install Python dependencies
pip3 install -r requirements.txt

# Note: Database connection details should be provided via CodeDeploy environment sourced from appspec.yaml
# or through AWS Systems Manager Parameter Store, Secrets Manager, or environment variables.
# The following assumes DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD, and PHOTOS_BUCKET 
# are set via CodeDeploy or environment configuration.

if [ -z "$DATABASE_HOST" ] || [ -z "$DATABASE_USER" ] || [ -z "$DATABASE_PASSWORD" ]; then
    echo "Warning: Database credentials not fully configured. Please set:"
    echo "  - DATABASE_HOST"
    echo "  - DATABASE_USER"
    echo "  - DATABASE_PASSWORD"
    echo "  - DATABASE_DB_NAME (defaults to 'employees')"
    echo "  - PHOTOS_BUCKET"
else
    echo "Initializing database..."
    export DATABASE_DB_NAME=${DATABASE_DB_NAME:-employees}
    
    # Create database tables
    cat database_create_tables.sql | \
    mysql -h "$DATABASE_HOST" -u "$DATABASE_USER" -p"$DATABASE_PASSWORD" \
          -e "CREATE DATABASE IF NOT EXISTS $DATABASE_DB_NAME;" && \
    cat database_create_tables.sql | \
    mysql -h "$DATABASE_HOST" -u "$DATABASE_USER" -p"$DATABASE_PASSWORD" "$DATABASE_DB_NAME"
    
    echo "Database initialized successfully"
fi

echo "Application setup completed"
