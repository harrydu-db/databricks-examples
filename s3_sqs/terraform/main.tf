provider "aws" {
  region = "us-west-2"
}

# Create SQS queue
resource "aws_sqs_queue" "s3_notification_queue" {
  name                      = var.sqs_queue_name
  message_retention_seconds = var.message_retention_seconds
  visibility_timeout_seconds = var.visibility_timeout_seconds
}

# Create SQS queue policy to allow S3 to send messages
resource "aws_sqs_queue_policy" "s3_notification_queue_policy" {
  queue_url = aws_sqs_queue.s3_notification_queue.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect    = "Allow"
        Principal = "*"
        Action    = "sqs:SendMessage"
        Resource  = aws_sqs_queue.s3_notification_queue.arn
        Condition = {
          ArnLike = {
            "aws:SourceArn" = "arn:aws:s3:::${var.s3_bucket_name}"
          }
        }
      }
    ]
  })
}

# Configure S3 bucket notification for existing bucket
resource "aws_s3_bucket_notification" "bucket_notification" {
  bucket = var.s3_bucket_name

  queue {
    queue_arn     = aws_sqs_queue.s3_notification_queue.arn
    events        = ["s3:ObjectCreated:*"]
    filter_prefix = var.s3_prefix
  }
} 