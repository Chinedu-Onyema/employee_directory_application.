#!/bin/bash
set -e

echo "Setting up application..."

cd /var/www/employee-directory

# Install Python dependencies
pip3 install -r requirements.txt

# Install and start MySQL locally
echo "Installing and configuring MySQL..."
sudo yum install -y mariadb105-server
sudo systemctl start mariadb
sudo systemctl enable mariadb

# Hardcoded secrets (replace with your actual values)
DB_USER="admin"
DB_PASSWORD="JmjX1SOL13YFY76Rv4dp"
DB_NAME="database-1"
S3_BUCKET="my-photos-albums-123"

# Set up MySQL database
# Set up MySQL database
echo "Initializing database..."
sudo mysql -e "CREATE DATABASE IF NOT EXISTS \`${DB_NAME}\`;"
sudo mysql -e "CREATE USER IF NOT EXISTS '${DB_USER}'@'localhost' IDENTIFIED BY '${DB_PASSWORD}';"
sudo mysql -e "GRANT ALL PRIVILEGES ON \`${DB_NAME}\`.* TO '${DB_USER}'@'localhost';"
sudo mysql -e "FLUSH PRIVILEGES;"

# Create database tables
if [ -f database_create_tables.sql ]; then
    cat database_create_tables.sql | sudo mysql ${DB_NAME}
    echo "Database tables created successfully"
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
Environment=\"DATABASE_HOST=localhost\"
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

