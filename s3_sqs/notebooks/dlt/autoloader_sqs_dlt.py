
source_path = "/Volumes/harry_du/dlt_sample/harrydu-one-env/lakehouse-iot-turbine/incoming_data"
schema = "id INT, timestamp TIMESTAMP, file_name STRING"
schemaLocation = "/Volumes/harry_du/dlt_sample/sample_data/logs/schema_csv"
checkpointLocation = "/Volumes/harry_du/dlt_sample/sample_data/logs/checkpoint"


autoloader_opts = {
    "cloudFiles.format": "csv",
    # "cloudFiles.maxFilesPerTrigger": "1",
    "cloudFiles.includeExistingFiles": "false",
    "cloudFiles.useNotifications": "true",
    "cloudFiles.queueUrl": "https://sqs.us-west-2.amazonaws.com/997819012307/s3_notification_queue_one_env_harrydu",
    "cloudFiles.inferColumnTypes": "true",
    "cloudFiles.schemaLocation": schemaLocation,
    "header": "true"
}

@dlt.table(
    name="sqs_test",  # Optional if specified elsewhere
    comment="Ingest data from S3 using Auto Loader with SQS notifications"
)
def bronze_table():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "csv")
        .option("cloudFiles.includeExistingFiles", "false")
        .option("cloudFiles.useNotifications", "true")
        .option("cloudFiles.queueUrl", "https://sqs.us-west-2.amazonaws.com/997819012307/s3_notification_queue_one_env_harrydu")
        .option("cloudFiles.inferColumnTypes", "true")
        .option("cloudFiles.schemaLocation", schemaLocation)
        .option("header", "true")
        .schema(schema)
        .load(source_path)
    )