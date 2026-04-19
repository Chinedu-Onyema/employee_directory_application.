#!/bin/bash
set -e

echo "Starting Flask application..."

# Source environment variables if they exist
if [ -f /etc/environment ]; then
    source /etc/environment
fi

cd /var/www/employee-directory

# Create systemd service if it doesn't exist
if [ ! -f /etc/systemd/system/employee-directory.service ]; then
    cat > /etc/systemd/system/employee-directory.service << EOF
[Unit]
Description=Employee Directory Flask Application
After=network.target

[Service]
Type=simple
User=ec2-user
WorkingDirectory=/var/www/employee-directory
Environment="FLASK_APP=application.py"
Environment="PATH=/usr/local/bin:/usr/bin:/bin"
EnvironmentFile=/etc/sysconfig/employee-directory
ExecStart=/usr/local/bin/flask run --host=0.0.0.0 --port=80
Restart=on-failure
RestartSec=10s

[Install]
WantedBy=multi-user.target
EOF
    
    # Create environment file directory if needed
    mkdir -p /etc/sysconfig
    
    # Create environment configuration file
    cat > /etc/sysconfig/employee-directory << EOF
FLASK_ENV=production
PHOTOS_BUCKET=${PHOTOS_BUCKET}
DATABASE_HOST=${DATABASE_HOST}
DATABASE_USER=${DATABASE_USER}
DATABASE_PASSWORD=${DATABASE_PASSWORD}
DATABASE_DB_NAME=${DATABASE_DB_NAME:-employees}
EOF
    
    # Enable and start the service
    systemctl daemon-reload
fi

systemctl enable employee-directory.service
systemctl start employee-directory.service

echo "Flask application started successfully"
