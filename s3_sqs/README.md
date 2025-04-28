# S3 to SQS Notification Setup

This Terraform configuration sets up an SQS queue that receives notifications when new files are added to a specific S3 bucket prefix.

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Terraform installed
3. Access to the S3 bucket `harrydu-sample-data2`

## Configuration

The configuration creates:
- An SQS queue to receive notifications
- SQS queue policy to allow S3 to send messages
- S3 bucket notification configuration

## Usage

1. Initialize Terraform:
```bash
terraform init
```

2. Review the planned changes:
```bash
terraform plan
```

3. Apply the configuration:
```bash
terraform apply
```

## Variables

You can customize the configuration by modifying the following variables in `variables.tf`:
- `aws_region`: AWS region (default: us-east-1)
- `s3_bucket_name`: Name of the S3 bucket (default: harrydu-sample-data2)
- `s3_prefix`: Prefix in the S3 bucket to monitor (default: lakehouse-iot-turbine/incoming_data/)
- `sqs_queue_name`: Name of the SQS queue (default: s3-file-notification-queue)
- `message_retention_seconds`: Message retention period (default: 86400)
- `visibility_timeout_seconds`: Visibility timeout (default: 300)

## Cleanup

To remove all created resources:
```bash
terraform destroy
``` 