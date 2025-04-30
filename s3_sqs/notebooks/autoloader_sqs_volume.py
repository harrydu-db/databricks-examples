# Databricks notebook source
source_path = "/Volumes/harry_du/dlt_sample/harrydu-one-env/lakehouse-iot-turbine/incoming_data"
schema = "id INT, timestamp TIMESTAMP, file_name STRING"
schemaLocation = "/Volumes/harry_du/dlt_sample/sample_data/logs/schema_csv"
checkpointLocation = "/Volumes/harry_du/dlt_sample/sample_data/logs/checkpoint"
bronze_table = "harry_du.dlt_sample.test"

# COMMAND ----------

# Run this if you need to clean up
spark.sql(f"DROP TABLE IF EXISTS {bronze_table}")
dbutils.fs.rm(schemaLocation, recurse=True)
dbutils.fs.rm(checkpointLocation, recurse=True)


# COMMAND ----------


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

df = (spark.readStream
      .format("cloudFiles")
      .options(**autoloader_opts)
      .schema(schema)
      .load(source_path)
    )
df.writeStream.outputMode("append").option("checkpointLocation",checkpointLocation).table(bronze_table)

# COMMAND ----------

df3 = spark.table(bronze_table)
print(df3.count())

# COMMAND ----------

# Stop all streams
for s in spark.streams.active:
  s.stop()