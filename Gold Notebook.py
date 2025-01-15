# Databricks notebook source
import json

dbutils.widgets.text("bronze_params", "")
dbutils.widgets.text("silver_params", "")

bronze_params = dbutils.widgets.get("bronze_params")
silver_params = dbutils.widgets.get("silver_params")

print(f"Raw bronze_params: {bronze_params}")
print(f"Raw silver_params: {silver_params}")

bronze_data = json.loads(bronze_params)

start_date = bronze_data.get("start_date", "")
end_date = bronze_data.get("end_date", "")
bronze_adls = bronze_data.get("bronze_adls", "")
silver_adls = bronze_data.get("silver_adls", "")
gold_adls = bronze_data.get("gold_adls", "")
silver_data = silver_params

print(f"start_date: {start_date}, End date: {end_date}")
print(f"Silver ADLS: {silver_adls}, Gold ADLS: {gold_adls}")

# COMMAND ----------

from pyspark.sql.functions import when, col, udf
from pyspark.sql.types import StringType
import reverse_geocoder as rg 
from datetime import date, timedelta

# COMMAND ----------

df = spark.read.parquet(silver_data).filter(col("time") < start_date)

# COMMAND ----------

display(df)

# COMMAND ----------

def get_country_code(lat, lon):

    try: 
        coordinates = (float(lat), float(lon))
        result = rg.search(coordinates)[0].get("cc")
        print(f"Processed coordnates: {coordinates} -> {result}")
        return result
    except Exception as e:  
        print(f"Error processing coordinates: {coordinates} -> {e}")
        return None

# COMMAND ----------

get_country_code_udf = udf(get_country_code, StringType())  


# COMMAND ----------

df_with_location = df.withColumn("country_code", get_country_code_udf(col("latitude"), col("longitude")))   

# COMMAND ----------

display(df_with_location.head())

# COMMAND ----------

# Significance classification
df_with_location_sig_class = df_with_location.withColumn(
    "sig_class",
    when(col("sig") < 100, "Low")
    .when((col("sig") >= 100) & (col("sig") < 500), "Moderate")
    .otherwise("High")
)
display(df_with_location_sig_class)

# COMMAND ----------

gold_output_path = f"{gold_adls}/earthquake_events_gold"

# COMMAND ----------

df_with_location_sig_class.write.mode("append").parquet(gold_output_path)   

# COMMAND ----------


