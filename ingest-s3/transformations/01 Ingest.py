import dlt
from pyspark.sql.functions import *

spark.conf.set("fs.s3a.access.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_access_key"))
spark.conf.set("fs.s3a.secret.key", dbutils.secrets.get("db-field-eng", "harrydu_sample_data_s3_aws_secret_key"))

# S3 path for source
source_path = "s3a://harrydu-sample-data2/lakehouse-iot-turbine/turbine/"

# Bronze layer: Load raw data using Auto Loader
@dlt.table (
    comment="Turbine details, with location, wind turbine model type etc",
    table_properties={"pipelines.constraint.correct_schema": "expect(_rescued_data IS NULL)"}
)
def turbine():
    return (
        spark.readStream.format("cloudFiles")
        .option("cloudFiles.format", "json")  # Change format if your source is CSV, Parquet, etc.
        .option("cloudFiles.inferColumnTypes", "true")
        .load(source_path)
    )