#!/bin/bash
set -e

echo "Validating service health..."

# Check if the service is running
if ! systemctl is-active --quiet employee-directory.service; then
    echo "ERROR: employee-directory service is not running"
    exit 1
fi

# Wait a moment for the service to fully start
sleep 2

# Check if the Flask app is responding on port 80
if curl -f http://localhost:80/ > /dev/null 2>&1; then
    echo "Service validation successful - Flask application is responding"
    exit 0
else
    echo "WARNING: Flask application is running but not responding to HTTP requests"
    echo "Checking service logs..."
    systemctl status employee-directory.service
    exit 1
fi
