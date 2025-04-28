# Databricks notebook source
source_path = "s3://harrydu-sample-data2/lakehouse-iot-turbine/incoming_data/"
spark.conf.set("fs.s3a.access.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_access_key"))
spark.conf.set("fs.s3a.secret.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_secret_key"))

# COMMAND ----------

schemaLocation = "/Volumes/harry_du/dlt_sample/sample_data/sqs_schema"
autoloader_opts = {
    "cloudFiles.format": "parquet",
    "cloudFiles.includeExistingFiles": "false",
    "cloudFiles.useNotifications": "true",
    "cloudFiles.awsAccessKey": dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_access_key"),
    "cloudFiles.awsSecretKey": dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_secret_key"),
    "cloudFiles.queueUrl": "https://sqs.us-west-2.amazonaws.com/693773272364/s3-file-notification-queue",
    "cloudFiles.inferColumnTypes": "true",
    "cloudFiles.schemaLocation": schemaLocation
}
# volume_path = "/Volumes/tdr_prod_nam/volumes/nvm_data/"

df = (spark.readStream
      .format("cloudFiles")
      .options(**autoloader_opts)
      .load(source_path)
    )

# COMMAND ----------

display(df)

# COMMAND ----------

display(df.select('_metadata.file_path').distinct())