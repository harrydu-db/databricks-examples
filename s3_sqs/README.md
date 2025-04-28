# S3 to SQS Notification Setup

This Terraform configuration sets up an SQS queue that receives notifications when new files are added to a specific S3 bucket prefix.

## Prerequisites

1. AWS CLI configured with appropriate credentials
2. Terraform installed
3. Access to the S3 bucket `harrydu-sample-data2`
4. Python 3.x installed
5. Databricks workspace access with:
   - Secrets scope `db-field-eng` configured
   - AWS credentials stored in secrets:
     - `harrydu_sample_data_s3_aws_access_key`
     - `harrydu_sample_data_s3_aws_secret_key`
   - Volume access to `/Volumes/harry_du/dlt_sample/sample_data/sqs_schema`

## Configuration

The configuration creates:
- An SQS queue to receive notifications
- SQS queue policy to allow S3 to send messages
- S3 bucket notification configuration

## Usage

### Terraform Setup

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

### File Upload Script

The `upload_to_s3.py` script can be used to upload files to the S3 bucket. It supports both single file and directory uploads.

#### Upload a Single File
```bash
./upload_to_s3.py /path/to/your/file
```

#### Upload All Files in a Directory
```bash
./upload_to_s3.py /path/to/your/directory
```

#### Upload with Custom Wait Time
```bash
./upload_to_s3.py /path/to/your/directory --wait-time 5
```

Features:
- Automatically sorts files in ascending order before uploading
- Configurable wait time between uploads (default: 3 seconds)
- Progress information for each upload
- Error handling for invalid paths

### Databricks Auto Loader Notebook

The `notebooks/autoloader_sqs.py` notebook demonstrates how to use Databricks Auto Loader with SQS notifications to process files as they are uploaded to S3.

#### Features
- Uses SQS notifications for efficient file detection
- Automatically processes new Parquet files in the S3 bucket
- Maintains schema information in a Databricks Volume
- Supports schema inference
- Tracks processed files using metadata

#### Configuration
1. Import the notebook into your Databricks workspace
2. Ensure secrets are configured in Databricks:
   ```python
   # AWS credentials are stored in Databricks secrets
   spark.conf.set("fs.s3a.access.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_access_key"))
   spark.conf.set("fs.s3a.secret.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_secret_key"))
   ```
3. Configure Auto Loader options:
   ```python
   autoloader_opts = {
       "cloudFiles.format": "parquet",
       "cloudFiles.includeExistingFiles": "false",
       "cloudFiles.useNotifications": "true",
       "cloudFiles.awsAccessKey": dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_access_key"),
       "cloudFiles.awsSecretKey": dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_secret_key"),
       "cloudFiles.queueUrl": "https://sqs.us-west-2.amazonaws.com/693773272364/s3-file-notification-queue",
       "cloudFiles.inferColumnTypes": "true",
       "cloudFiles.schemaLocation": "/Volumes/harry_du/dlt_sample/sample_data/sqs_schema"
   }
   ```

#### Usage
1. Run the notebook in your Databricks workspace
2. The Auto Loader will automatically detect new files through SQS notifications
3. Processed files can be monitored using the metadata columns
4. Use `display(df.select('_metadata.file_path').distinct())` to view processed files

## Variables

You can customize the configuration by modifying the following variables in `variables.tf`:
- `aws_region`: AWS region (default: us-west-2)
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