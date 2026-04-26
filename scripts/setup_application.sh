#!/bin/bash
set -e

echo "Setting up application..."

cd /var/www/employee-directory

# Install Python dependencies
pip3 install -r requirements.txt

# Hardcoded secrets (replace with your actual values)
DB_HOST="employees.c1408oeoalyx.eu-north-1.rds.amazonaws.com"
DB_USER="admin"
DB_PASSWORD="qLlP1O2dW3InDQVmBGqP"
DB_NAME="employees"
S3_BUCKET="my-photos-albums-123"

# Create database tables on RDS
echo "Creating database on RDS if it doesn't exist..."
mysql -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" -e "CREATE DATABASE IF NOT EXISTS employees;"

# Create database tables on RDS
echo "Initializing RDS database tables..."
if [ -f database_create_tables.sql ]; then
    mysql -h "${DB_HOST}" -u "${DB_USER}" -p"${DB_PASSWORD}" "${DB_NAME}" < database_create_tables.sql
    echo "Database tables created successfully on RDS"
fi

# Create systemd service file
echo "Creating systemd service file..."
sudo bash -c "cat > /etc/systemd/system/employee-directory.service <<EOF
[Unit]
Description=Employee Directory Flask Application
After=network.target

[Service]
User=root
WorkingDirectory=/var/www/employee-directory
Environment=\"FLASK_APP=application.py\"
Environment=\"DATABASE_HOST=${DB_HOST}\"
Environment=\"DATABASE_USER=${DB_USER}\"
Environment=\"DATABASE_PASSWORD=${DB_PASSWORD}\"
Environment=\"DATABASE_DB_NAME=${DB_NAME}\"
Environment=\"PHOTOS_BUCKET=${S3_BUCKET}\"
ExecStart=/usr/local/bin/flask run --host=0.0.0.0 --port=80
Restart=always

[Install]
WantedBy=multi-user.target
EOF"

echo "Application setup completed"


