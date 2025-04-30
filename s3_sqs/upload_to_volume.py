#!/usr/bin/env python3

import os
import sys
import argparse
import time
import subprocess
from pathlib import Path

# Volume configuration
# TODO: change to your own volume path
volume_path = "dbfs:/Volumes/harry_du/dlt_sample/harrydu-one-env/lakehouse-iot-turbine/incoming_data/"

def copy_file_to_volume(file_path, volume_path):
    """
    Copy a file to Databricks Volume using databricks fs cp command
    
    Args:
        file_path (str): Local path to the file to upload
        volume_path (str): Target path in Databricks Volume
    """
    try:
        # Construct the databricks fs cp command
        cmd = ["databricks", "fs", "cp", file_path, volume_path]
        
        # Execute the command
        result = subprocess.run(cmd, capture_output=True, text=True)
        
        if result.returncode == 0:
            print(f"Successfully copied {file_path} to {volume_path}")
        else:
            print(f"Error copying file: {result.stderr}")
            sys.exit(1)
            
    except Exception as e:
        print(f"Error executing databricks command: {str(e)}")
        sys.exit(1)

def copy_directory_to_volume(directory_path, volume_path, wait_time=3):
    """
    Copy all files in a directory to Databricks Volume
    
    Args:
        directory_path (str): Local path to the directory
        volume_path (str): Target path in Databricks Volume
        wait_time (int): Wait time in seconds between copies
    """
    # Get all files in the directory and sort them
    files = sorted([f for f in Path(directory_path).glob('*') if f.is_file()])
    
    if not files:
        print(f"No files found in directory: {directory_path}")
        return
    
    print(f"Found {len(files)} files to copy")
    
    # Copy each file with wait time in between
    for file_path in files:
        copy_file_to_volume(str(file_path), volume_path)
        if wait_time > 0:
            print(f"Waiting {wait_time} seconds before next copy...")
            time.sleep(wait_time)

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Copy a file or directory to Databricks Volume')
    parser.add_argument('path', help='Path to the file or directory to copy')
    parser.add_argument('--wait-time', type=int, default=0, help='Wait time in seconds between copies (for directories)')
    args = parser.parse_args()
    

    
    # Check if path exists
    if not os.path.exists(args.path):
        print(f"Error: Path {args.path} does not exist")
        sys.exit(1)
    
    # Copy based on whether it's a file or directory
    if os.path.isfile(args.path):
        copy_file_to_volume(args.path, volume_path)
    elif os.path.isdir(args.path):
        copy_directory_to_volume(args.path, volume_path, args.wait_time)
    else:
        print(f"Error: {args.path} is neither a file nor a directory")
        sys.exit(1)

if __name__ == "__main__":
    main() 