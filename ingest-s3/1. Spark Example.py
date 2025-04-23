# Databricks notebook source
# MAGIC %md
# MAGIC ## Configure Secret
# MAGIC
# MAGIC Put secret in Scope
# MAGIC
# MAGIC Run this to add access key
# MAGIC ```bash
# MAGIC databricks secrets put-secret db-field-eng harrydu_sample_data_s3_aws_access_key
# MAGIC ```
# MAGIC Run this to add secret key
# MAGIC ```bash
# MAGIC databricks secrets put-secret db-field-eng harrydu_sample_data_s3_aws_secret_key
# MAGIC ```
# MAGIC

# COMMAND ----------

spark.conf.set("fs.s3a.access.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_access_key"))
spark.conf.set("fs.s3a.secret.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_secret_key"))

# COMMAND ----------

# Read data from S3
df = spark.read.format("json").load("s3a://harrydu-sample-data2/lakehouse-iot-turbine/turbine/")
display(df)

# COMMAND ----------

df = spark.table("harry_du.dlt_sample.turbine")
display(df)

# COMMAND ----------

df.printSchema()
