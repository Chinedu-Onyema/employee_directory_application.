#!/bin/bash
set -e

echo "Stopping Flask application..."

# Stop the service if it exists
if systemctl is-active --quiet employee-directory.service; then
    systemctl stop employee-directory.service
    echo "Flask application stopped successfully"
else
    echo "Flask application is not running"
fi
