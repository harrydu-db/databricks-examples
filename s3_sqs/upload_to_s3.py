#!/usr/bin/env python3

import boto3
import os
import sys
import argparse

def upload_file_to_s3(file_path, bucket_name, s3_prefix):
    """
    Upload a file to S3 bucket with specified prefix
    
    Args:
        file_path (str): Local path to the file to upload
        bucket_name (str): Name of the S3 bucket
        s3_prefix (str): Prefix in the S3 bucket
    """
    # Create S3 client
    s3_client = boto3.client('s3')
    
    # Get the file name from the path
    file_name = os.path.basename(file_path)
    
    # Construct the S3 key
    s3_key = f"{s3_prefix}{file_name}"
    
    try:
        # Upload the file
        s3_client.upload_file(file_path, bucket_name, s3_key)
        print(f"Successfully uploaded {file_path} to s3://{bucket_name}/{s3_key}")
    except Exception as e:
        print(f"Error uploading file: {str(e)}")
        sys.exit(1)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Upload a file to S3 bucket')
    parser.add_argument('file_path', help='Path to the file to upload')
    args = parser.parse_args()
    
    # S3 configuration
    bucket_name = 'harrydu-sample-data2'
    s3_prefix = 'lakehouse-iot-turbine/incoming_data/'
    
    # Check if file exists
    if not os.path.isfile(args.file_path):
        print(f"Error: File {args.file_path} does not exist")
        sys.exit(1)
    
    # Upload the file
    upload_file_to_s3(args.file_path, bucket_name, s3_prefix)

if __name__ == "__main__":
    main() 