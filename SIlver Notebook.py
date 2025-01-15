# Databricks notebook source
import json

bronze_params =  dbutils.widgets.get("bronze_params")
print(f"Raw bromze_params: {bronze_params}")

output_data = json.loads(bronze_params)

start_date = output_data.get("start_date", "")
end_date = output_data.get("end_date", "")
bronze_adls = output_data.get("bronze_adls", "")
silver_adls = output_data.get("silver_adls", "")
gold_adls = output_data.get("gold_adls", "")
print(f"start_date: {start_date}, Bronze ADLS: {bronze_adls}")

# COMMAND ----------

from pyspark.sql.functions import col, isnull, when
from pyspark.sql.types import TimestampType
from datetime import date, timedelta

# COMMAND ----------

#Load data into a spark dataframe
df = spark.read.option("multiline", "true").json(f"{bronze_adls}/{start_date}_earthquake_data.json")

# COMMAND ----------

#Reshape dataframe
df = (
    df
    .select(
        'id',
        col('geometry.coordinates').getItem(0).alias('longitude'), 
        col('geometry.coordinates').getItem(1).alias('latitude'),
        col('geometry.coordinates').getItem(2).alias('elevation'),
        col('properties.title').alias('title'),
        col('properties.sig').alias('sig'),
        col('properties.mag').alias('magnitude'),
        col('properties.time').alias('time'),
        col('properties.updated').alias('updated')
    )
)

# COMMAND ----------

df = (
    df
    .withColumn('longitude', when(isnull(col('longitude')), 0).otherwise(col('longitude')))
    .withColumn('latitude', when(isnull(col('latitude')), 0).otherwise(col('latitude')))
    .withColumn('time', when(isnull(col('time')), 0).otherwise(col('time')))
)

# COMMAND ----------

display(df)

# COMMAND ----------

df = (
    df
    .withColumn('time', (col('time') / 1000).cast(TimestampType()))
    .withColumn('updated', (col('updated') / 1000).cast(TimestampType()))
)

# COMMAND ----------

display(df.head())

# COMMAND ----------

#Save the transformed dataframe to Silver container
silver_output_path = f"{silver_adls}/earthquake_events_silver/"

# COMMAND ----------

df.write.mode('append').parquet(silver_output_path)

# COMMAND ----------

dbutils.notebook.exit(silver_output_path)
