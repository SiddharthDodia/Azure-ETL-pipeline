# Databricks notebook source
# Mounting adlsg2

containers = ["bronze", "silver", "gold"]
adls_path = {container: f"abfss://{container}@adlsg2project1sid.dfs.core.windows.net/" for container in containers}

bronze_adls = adls_path["bronze"]
silver_adls = adls_path["silver"]
gold_adls = adls_path["gold"]

dbutils.fs.ls(bronze_adls)
dbutils.fs.ls(silver_adls)
dbutils.fs.ls(gold_adls)

# COMMAND ----------

import requests
import json
from datetime import date, timedelta

# COMMAND ----------

# Get parameters
dbutils.widgets.text("start_date", "")
dbutils.widgets.text("end_date", "")

start_date = dbutils.widgets.get("start_date")
end_date = dbutils.widgets.get("end_date")

# COMMAND ----------

url = f"https://earthquake.usgs.gov/fdsnws/event/1/query?format=geojson&starttime={start_date}&endtime={end_date}"



# COMMAND ----------

try:
    response = requests.get(url)

    response.raise_for_status() #Raise HTTP Error for bad responses
    data = response.json().get("features", [])

    if not data : 
        print("No data returned for the specific date range")
    else: 
        file_path = f"{bronze_adls}/{start_date}_earthquake_data.json"

        json_data = json.dumps(data, indent=4)
        dbutils.fs.put(file_path, json_data, overwrite = True)
        print(f"Data written to {file_path}")
except requests.exceptions.RequestException as e:
    print(f"Error fetching data from API: {e}")

# COMMAND ----------

output_data = {
    "start_date": start_date,
    "end_date": end_date,
    "bronze_adls": bronze_adls,
    "silver_adls": silver_adls,
    "gold_adls": gold_adls
}

output_json = json.dumps(output_data)
print(f"Serialized JSON: {output_json}")

dbutils.notebook.exit(output_json)
