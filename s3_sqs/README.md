# S3 to SQS Notification and File Processing Setup

## Notice
This code is provided as-is without any warranties or guarantees. Use at your own risk. The author is not responsible for any damages or issues that may arise from using this code.

## Prerequisites

1. AWS CLI configured with appropriate credentials:
   ```bash
   # Install AWS CLI if not already installed
   # For macOS:
   brew install awscli
   
   # Configure AWS CLI
   aws configure
   # Enter your AWS Access Key ID
   # Enter your AWS Secret Access Key
   # Enter default region (us-west-2)
   # Enter default output format (json)
   
   # Verify configuration
   aws configure list
   ```

2. Required Software:
   - Terraform
   - Python 3.x
   - Required Python packages
     ```bash
     cd ..
     # Create and activate a virtual environment (recommended)
     python -m venv .venv
     source .venv/bin/activate  # On Windows: .venv\Scripts\activate
     
     # Install required packages
     pip install -r requirements.txt
     ```

3. AWS Access:
   - Access to S3 bucket `harrydu-sample-data2`
   - Access to S3 bucket `one-env-uc-external-location`

4. Databricks Workspace Access:
   - Secrets scope `db-field-eng` configured
   - AWS credentials stored in secrets:
     - `harrydu_sample_data_s3_aws_access_key`
     - `harrydu_sample_data_s3_aws_secret_key`
   - Volume access to `/Volumes/harry_du/dlt_sample/sample_data/sqs_schema`

## Infrastructure Setup

### Terraform Configuration

The Terraform configuration sets up:
- An SQS queue to receive notifications
- SQS queue policy to allow S3 to send messages
- S3 bucket notification configuration

#### Usage

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

#### Customization

You can customize the configuration by modifying the following variables in `variables.tf`:
- `aws_region`: AWS region (default: us-west-2)
- `s3_bucket_name`: Name of the S3 bucket (default: harrydu-sample-data2)
- `s3_prefix`: Prefix in the S3 bucket to monitor (default: lakehouse-iot-turbine/incoming_data/)
- `sqs_queue_name`: Name of the SQS queue (default: s3-file-notification-queue)
- `message_retention_seconds`: Message retention period (default: 86400)
- `visibility_timeout_seconds`: Visibility timeout (default: 300)

## File Management Tools

### 1. CSV File Generation (`generate_csv_files.py`)

Generates CSV files with sample data in the `temp_csv_files` directory.

#### Usage
```bash
python3 generate_csv_files.py <start_id> <number_of_files>


#### Arguments
- `start_id`: Starting ID for the sequence of files
- `number_of_files`: Number of files to generate

#### Example
```bash
# Generate 5 files starting from ID 1
python3 generate_csv_files.py 1 5
```

#### Output Format
```csv
id,timestamp,file_name
1,2024-04-28T12:34:56.789012,data_1.csv
```

### 2. Combined Generation and Sync (`generate_and_sync.sh`)

Combines CSV generation and S3 sync operations into a single command.
TODO: Change to your bucket name and filepath

#### Usage
```bash
./generate_and_sync.sh <start_id> <number_of_files>
```

#### Process
1. Generates CSV files in the `temp_csv_files` directory
2. Changes to the `temp_csv_files` directory
3. Syncs files to S3 using `aws s3 sync` with the `--delete` flag
4. Returns to the original directory


### 3. File Upload Script (`upload_to_s3.py`)

Uploads files to the S3 bucket, supporting both single file and directory uploads.

#### Usage
```bash
# Upload a single file
./upload_to_s3.py /path/to/your/file

# Upload all files in a directory
./upload_to_s3.py /path/to/your/directory

# Upload with custom wait time
./upload_to_s3.py /path/to/your/directory --wait-time 5
```

## S3 Management

### List Files
```bash
aws s3 ls s3://harrydu-sample-data2/lakehouse-iot-turbine/incoming_data/ --recursive
```

### Cleanup
```bash
# Delete all files
aws s3 rm s3://harrydu-sample-data2/lakehouse-iot-turbine/incoming_data/ --recursive

# Delete specific file types
aws s3 rm s3://harrydu-sample-data2/lakehouse-iot-turbine/incoming_data/ --recursive --exclude "*" --include "*.parquet"
```

## Databricks Integration

### Auto Loader Configuration

The `notebooks/autoloader_sqs.py` notebook demonstrates how to use Databricks Auto Loader with SQS notifications.

#### Features
- Uses SQS notifications for efficient file detection
- Automatically processes new Parquet files
- Maintains schema information in a Databricks Volume
- Supports schema inference
- Tracks processed files using metadata

#### Setup
1. Import the notebook into your Databricks workspace
2. Configure secrets:
   ```python
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

## Cleanup

1. Remove Terraform resources:
```bash
terraform destroy
```

2. Cleanup S3 folder:
```bash
aws s3 rm s3://harrydu-sample-data2/lakehouse-iot-turbine/incoming_data/ --recursive
```

## References
- [Ingestion from S3 Example](../ingest-s3/)
- [What is Auto Loader file notification mode?](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-notification-mode)
- [Required Permission for configuration file notification for S3](https://docs.databricks.com/aws/en/ingestion/cloud-object-storage/auto-loader/file-notification-mode#required-permissions-for-configuring-file-notification-for-amazon-s3)
