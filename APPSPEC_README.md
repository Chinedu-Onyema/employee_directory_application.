# AWS CodeDeploy AppSpec Configuration

This repository includes an AWS CodeDeploy AppSpec file (`appspec.yaml`) for automated deployment of the Employee Directory Flask application.

## Files

- **appspec.yaml** - Main CodeDeploy configuration file
- **scripts/** - Deployment lifecycle scripts
  - `install_dependencies.sh` - Installs system packages and Python dependencies
  - `setup_application.sh` - Initializes the application and database
  - `start_server.sh` - Starts the Flask application using systemd
  - `stop_server.sh` - Stops the Flask application
  - `validate_service.sh` - Validates that the service is running and responsive

## Prerequisites

1. **AWS CodeDeploy Agent** must be installed on the EC2 instance
2. **Amazon Linux 2** or compatible OS with `yum` package manager
3. **IAM Role** on the EC2 instance with appropriate permissions for:
   - Accessing the CodeDeploy artifact bucket
   - Accessing RDS MySQL database (if applicable)
   - Accessing S3 bucket for photos (PHOTOS_BUCKET)
   - CloudWatch Logs (for logging)

## Environment Variables

The following environment variables must be configured before deployment. Set them in your CodeDeploy deployment configuration:

- **DATABASE_HOST** - MySQL server hostname/IP
- **DATABASE_USER** - MySQL user
- **DATABASE_PASSWORD** - MySQL password
- **DATABASE_DB_NAME** - Database name (defaults to `employees`)
- **PHOTOS_BUCKET** - S3 bucket name for storing employee photos

### Setting Environment Variables

You can set these variables in several ways:

1. **AWS CodeDeploy appspec.yaml environment section** (if using newer version)
2. **Systems Manager Parameter Store** - Recommended for sensitive data
3. **AWS Secrets Manager** - Best practice for credentials
4. **Direct environment configuration** - Less secure, not recommended for passwords

## Deployment Steps

1. **Commit the appspec.yaml and scripts/ directory to your repository**

2. **Create a CodeDeploy Application**:
   ```bash
   aws deploy create-app --application-name employee-directory
   ```

3. **Create a CodeDeploy Deployment Group**:
   ```bash
   aws deploy create-deployment-group \
     --application-name employee-directory \
     --deployment-group-name prod-deployment \
     --deployment-config-name CodeDeployDefault.AllAtOnce \
     --service-role-arn arn:aws:iam::ACCOUNT_ID:role/CodeDeployRole \
     --ec2-tag-filters Key=Environment,Value=production
   ```

4. **Create a deployment**:
   ```bash
   aws deploy create-deployment \
     --application-name employee-directory \
     --deployment-group-name prod-deployment \
     --s3-location s3://my-bucket/employee-directory.zip \
     --deployment-config-name CodeDeployDefault.AllAtOnce
   ```

## Deployment Lifecycle

The AppSpec file defines the following lifecycle events:

1. **BeforeInstall** - Installs system packages and Python dependencies
2. **AfterInstall** - Sets up the application and initializes the database
3. **ApplicationStart** - Starts the Flask application via systemd
4. **ApplicationStop** - Stops the running application
5. **ValidateService** - Verifies the application is running and responding

## Service Management

After deployment, the Flask application runs as a systemd service:

```bash
# Check service status
systemctl status employee-directory.service

# View logs
journalctl -u employee-directory.service -f

# Manually start/stop
systemctl start employee-directory.service
systemctl stop employee-directory.service

# Enable auto-start on reboot
systemctl enable employee-directory.service
```

## Troubleshooting

### Check deployment logs
```bash
# CodeDeploy logs
cat /var/log/codedeploy-agent/codedeploy-agent.log

# CodeDeploy deployment logs
ls /var/log/codedeploy-agent/deployments/
```

### Check application logs
```bash
journalctl -u employee-directory.service -n 50 -f
```

### Common Issues

- **Database connection errors**: Verify DATABASE_HOST, DATABASE_USER, DATABASE_PASSWORD are set correctly and network connectivity to the database
- **Port 80 access denied**: Ensure the EC2 instance has inbound rules allowing port 80
- **Service not starting**: Check SystemD service logs with `journalctl -xe`
- **Permission denied on scripts**: Ensure scripts are executable (should be set by CodeDeploy)

## Notes

- The Flask application runs on port 80 as root (via systemd). Consider running on a higher port (e.g., 8080) and using a reverse proxy (nginx/Apache) in production.
- Database credentials should be stored securely using AWS Secrets Manager or Systems Manager Parameter Store, not hardcoded.
- Ensure proper VPC and security group configurations to allow database and S3 access.
