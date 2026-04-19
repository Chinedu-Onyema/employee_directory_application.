#!/bin/bash
set -e

echo "Installing system dependencies..."

# Update system packages
yum -y update

# Install Python3, MySQL client, and basic tools
yum -y install python3 python3-pip mysql

# Install epel-release for additional packages
amazon-linux-extras install -y epel

# Install stress testing tool
yum -y install stress

echo "Dependencies installed successfully"
