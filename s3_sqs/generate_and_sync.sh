#!/bin/bash

# Check if both arguments are provided
if [ "$#" -ne 2 ]; then
    echo "Usage: $0 <start_id> <number_of_files>"
    exit 1
fi

# Store arguments
START_ID=$1
NUMBER_OF_FILES=$2

# Generate CSV files
echo "Generating CSV files..."
python3 generate_csv_files.py $START_ID $NUMBER_OF_FILES

# Check if generation was successful
if [ $? -ne 0 ]; then
    echo "Error generating CSV files"
    exit 1
fi

# Change to temp_csv_files directory
cd temp_csv_files

# Sync to S3
echo "Syncing files to S3..."
# TODO: change to your own bucket name and prefix
aws s3 sync . s3://one-env-uc-external-location/harrydu/lakehouse-iot-turbine/incoming_data/ --delete

# Check if sync was successful
if [ $? -ne 0 ]; then
    echo "Error syncing files to S3"
    exit 1
fi

# Return to original directory
cd ..

echo "Operation completed successfully" 