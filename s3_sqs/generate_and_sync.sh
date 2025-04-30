#!/bin/bash

# Check if at least one argument is provided
if [ "$#" -lt 1 ]; then
    echo "Usage: $0 <start_id> [number_of_files]"
    echo "If number_of_files is not provided, will continuously generate one file at a time with 3-second wait"
    exit 1
fi

# Store arguments
START_ID=$1
NUMBER_OF_FILES=$2

# Define S3 destination
S3_DESTINATION="s3://one-env-uc-external-location/harrydu/lakehouse-iot-turbine/incoming_data/"

# Function to generate and sync a single file
generate_and_sync_single() {
    local current_id=$1
    echo "Generating file with ID: $current_id"
    python3 generate_csv_files.py $current_id 1
    
    if [ $? -ne 0 ]; then
        echo "Error generating CSV file"
        exit 1
    fi
    
    # Change to temp_csv_files directory
    cd temp_csv_files
    
    # Sync to S3
    echo "Syncing file to S3..."
    aws s3 sync . $S3_DESTINATION --delete
    
    if [ $? -ne 0 ]; then
        echo "Error syncing files to S3"
        exit 1
    fi
    
    # Return to original directory
    cd ..
    
    echo "File $current_id generated and synced successfully"
}

# If number_of_files is not provided, continuously generate files
if [ -z "$NUMBER_OF_FILES" ]; then
    echo "Starting continuous file generation from ID $START_ID"
    echo "Press Ctrl+C to stop"
    
    current_id=$START_ID
    while true; do
        generate_and_sync_single $current_id
        echo "Waiting 3 seconds before next file..."
        sleep 3
        current_id=$((current_id + 1))
    done
else
    # Generate specified number of files
    for ((i=0; i<NUMBER_OF_FILES; i++)); do
        current_id=$((START_ID + i))
        generate_and_sync_single $current_id
    done
    echo "Operation completed successfully"
fi 