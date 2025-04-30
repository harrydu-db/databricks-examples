#!/usr/bin/env python3

import os
import sys
import argparse
import time
import csv
from datetime import datetime
from pathlib import Path

def create_csv_file(file_id, output_dir):
    """
    Create a CSV file with id and timestamp
    
    Args:
        file_id (int): Sequential ID for the file
        output_dir (str): Directory to save the CSV file
    Returns:
        str: Path to the created CSV file
    """
    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    
    # Create the file path
    file_path = os.path.join(output_dir, f"data_{file_id}.csv")
    
    # Create CSV content
    data = {
        'id': file_id,
        'timestamp': datetime.now().isoformat(),
        'file_name': f"data_{file_id}.csv"
    }
    
    # Write the CSV file with header
    with open(file_path, 'w', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=['id', 'timestamp', 'file_name'])
        writer.writeheader()
        writer.writerow(data)
    
    return file_path

def main():
    # Set up argument parser
    parser = argparse.ArgumentParser(description='Generate CSV files in temporary directory')
    parser.add_argument('start_id', type=int, help='Starting ID for the sequence')
    parser.add_argument('number_of_files', type=int, help='Number of files to generate')
    args = parser.parse_args()
    
    # Create temporary directory for CSV files
    temp_dir = "temp_csv_files"
    
    try:
        # Generate files
        for i in range(args.start_id, args.start_id + args.number_of_files):
            # Create CSV file
            file_path = create_csv_file(i, temp_dir)
            print(f"Created CSV file: {file_path}")
            
                
    except Exception as e:
        print(f"Error generating files: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    main() 