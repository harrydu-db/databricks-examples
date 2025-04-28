#!/usr/bin/env python3

import boto3
import os
import sys
import argparse
import time
from pathlib import Path

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

def upload_directory_to_s3(directory_path, bucket_name, s3_prefix, wait_time=3):
    """
    Upload all files in a directory to S3 bucket with specified prefix
    
    Args:
        directory_path (str): Local path to the directory
        bucket_name (str): Name of the S3 bucket
        s3_prefix (str): Prefix in the S3 bucket
        wait_time (int): Wait time in seconds between uploads
    """
    # Get all files in the directory and sort them
    files = sorted([f for f in Path(directory_path).glob('*') if f.is_file()])
    
    if not files:
        print(f"No files found in directory: {directory_path}")
        return
    
    print(f"Found {len(files)} files to upload")
    
    # Upload each file with wait time in between
    for file_path in files:
        upload_file_to_s3(str(file_path), bucket_name, s3_prefix)
        if wait_time > 0:
            print(f"Waiting {wait_time} seconds before next upload...")
            time.sleep(wait_time)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Upload a file or directory to S3 bucket')
    parser.add_argument('path', help='Path to the file or directory to upload')
    parser.add_argument('--wait-time', type=int, default=3, help='Wait time in seconds between uploads (for directories)')
    args = parser.parse_args()
    
    # S3 configuration
    bucket_name = 'harrydu-sample-data2'
    s3_prefix = 'lakehouse-iot-turbine/incoming_data/'
    
    # Check if path exists
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        sys.exit(1)
    
    # Upload based on whether it's a file or directory
    if os.path.isfile(args.path):
        upload_file_to_s3(args.path, bucket_name, s3_prefix)
    elif os.path.isdir(args.path):
        upload_directory_to_s3(args.path, bucket_name, s3_prefix, args.wait_time)
    else:
        print(f"Error: {args.path} is neither a file nor a directory")
        sys.exit(1)

if __name__ == "__main__":
    main() 