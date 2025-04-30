variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-west-2"
}

variable "s3_bucket_name" {
  description = "Name of the S3 bucket"
  type        = string
  default     = "harrydu-sample-data2"
}

variable "s3_prefix" {
  description = "Prefix in the S3 bucket to monitor"
  type        = string
  default     = "lakehouse-iot-turbine/incoming_data/"
}

variable "sqs_queue_name" {
  description = "Name of the SQS queue"
  type        = string
  default     = "s3-file-notification-queue"
}

variable "message_retention_seconds" {
  description = "Message retention period in seconds"
  type        = number
  default     = 86400  # 24 hours
}

variable "visibility_timeout_seconds" {
  description = "Visibility timeout in seconds"
  type        = number
  default     = 300    # 5 minutes
} 