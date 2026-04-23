#!/bin/bash
set -e

echo "Installing system dependencies..."

# Update system packages
yum -y update

# Install Python3, Mariadb client, and basic tools
yum -y install python3 python3-pip mariadb105

# Install stress testing tool
yum -y install stress

echo "Dependencies installed successfully"
