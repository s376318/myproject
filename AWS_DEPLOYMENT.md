# AWS Elastic Beanstalk Configuration

This document provides instructions for deploying the Vlog Application to AWS Elastic Beanstalk.

## Prerequisites

1. AWS Account with Elastic Beanstalk access
2. AWS CLI installed and configured
3. EB CLI (Elastic Beanstalk CLI) installed
4. Python 3.9+
5. All dependencies installed from requirements.txt

## Deployment Steps

### 1. Initialize Elastic Beanstalk Application

```bash
# Navigate to project directory
cd c:\Users\burha\Desktop\myproject

# Initialize EB application (run from project root)
eb init -p python-3.11 vlog-application --region us-east-1
```

### 2. Create Environment Configuration

Create `.ebextensions/django.config`:

```yaml
option_settings:
  aws:elasticbeanstalk:container:python:
    WSGIPath: vlogproject.wsgi:application
  aws:elasticbeanstalk:application:environment:
    PYTHONPATH: /var/app/current:$PYTHONPATH
  aws:autoscaling:launchconfiguration:
    IamInstanceProfile: aws-elasticbeanstalk-ec2-role
    
container_commands:
  01_migrate:
    command: "source /var/app/venv/*/bin/activate && python manage.py migrate --noinput"
    leader_only: true
  02_collectstatic:
    command: "source /var/app/venv/*/bin/activate && python manage.py collectstatic --noinput"

commands:
  01_pip_upgrade:
    command: "source /var/app/venv/*/bin/activate && pip install --upgrade pip"
```

### 3. Create Environment

```bash
# Create a new environment
eb create vlog-env --instance-type t2.micro
```

### 4. Deploy Application

```bash
# Deploy the application
eb deploy

# Check deployment status
eb status

# View logs
eb logs
```

### 5. Environment Variables

Set environment variables on AWS:

```bash
eb setenv \
  DEBUG=False \
  SECRET_KEY='your-secret-key-here' \
  ALLOWED_HOSTS='yourdomain.elasticbeanstalk.com'
```

### 6. Database Setup

For production, use AWS RDS (Relational Database Service):

1. Create RDS PostgreSQL instance
2. Update `DATABASES` in settings.py to use RDS endpoint
3. Run migrations: `eb ssh` and `python manage.py migrate`

### 7. Static Files and Media

Use AWS S3 for static files and media:

```bash
pip install boto3 django-storages
```

Update settings.py:

```python
if not DEBUG:
    # S3 Configuration
    AWS_STORAGE_BUCKET_NAME = 'your-bucket-name'
    AWS_S3_REGION_NAME = 'us-east-1'
    AWS_S3_CUSTOM_DOMAIN = f'{AWS_STORAGE_BUCKET_NAME}.s3.amazonaws.com'
    STATIC_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/static/'
    MEDIA_URL = f'https://{AWS_S3_CUSTOM_DOMAIN}/media/'
    STATIC_ROOT = 'static/'
    
    DEFAULT_FILE_STORAGE = 'storages.backends.s3boto3.S3Boto3Storage'
    STATICFILES_STORAGE = 'storages.backends.s3boto3.S3StaticStorage'
```

### 8. SSL/HTTPS Setup

In `.ebextensions/https-instance.config`:

```yaml
option_settings:
  aws:elbv2:listener:443:
    InstancePort: 80
    InstanceProtocol: HTTP
    Protocol: HTTPS
    SSLCertificateArns: arn:aws:acm:region:account-id:certificate/certificate-id
  aws:elasticbeanstalk:xray:
    XRayEnabled: false
```

### 9. Monitor Application

```bash
# Monitor in real-time
eb open

# SSH into instance
eb ssh

# Check CPU and memory usage
eb health
```

### 10. Scaling Configuration

In `.ebextensions/scaling.config`:

```yaml
option_settings:
  aws:autoscaling:asg:
    MinSize: 1
    MaxSize: 5
  aws:autoscaling:trigger:
    MeasureName: CPUUtilization
    Statistic: Average
    Unit: Percent
    UpperThreshold: 70
    LowerThreshold: 30
```

## Security Considerations

1. **SECRET_KEY**: Never commit to version control
   ```bash
   export SECRET_KEY=$(python -c 'import secrets; print(secrets.token_urlsafe(50))')
   eb setenv SECRET_KEY=$SECRET_KEY
   ```

2. **Database Credentials**: Use AWS RDS with security groups
3. **HTTPS**: Always enable HTTPS in production
4. **ALLOWED_HOSTS**: Set to your domain name
5. **DEBUG**: Set to False in production

## Troubleshooting

### Check logs:
```bash
eb logs --all
```

### SSH into instance:
```bash
eb ssh
```

### View environment info:
```bash
eb printenv
```

### Rebuild environment:
```bash
eb rebuild
```

### Terminate environment:
```bash
eb terminate vlog-env
```

## Cost Estimation

- **EC2 Instance (t2.micro)**: ~$0.01/hour (eligible for free tier)
- **RDS Database**: ~$0.017/hour for small instance
- **S3 Storage**: ~$0.023 per GB
- **Data Transfer**: Various rates

## Useful Resources

- [Elastic Beanstalk Django Documentation](https://docs.aws.amazon.com/elasticbeanstalk/latest/dg/create-deploy-python-django.html)
- [AWS RDS Documentation](https://docs.aws.amazon.com/rds/)
- [AWS S3 Documentation](https://docs.aws.amazon.com/s3/)
- [Django-Storages Documentation](https://django-storages.readthedocs.io/)
