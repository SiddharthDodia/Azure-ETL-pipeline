ETL Pipeline for Earthquake Data in Azure

Project Overview 🚀🌍🔧

This project demonstrates the implementation of a robust ETL (Extract, Transform, Load) pipeline in Azure, leveraging several cutting-edge services to manage, transform, and analyze earthquake data from the Earthquake Catalog API. 🌟🌐✨

Key Features:

Data Ingestion: Data is ingested daily from the Earthquake Catalog API using Databricks.

Data Transformation: The ingested data is processed and transformed in Databricks to derive meaningful insights.

Medallion Architecture: Data is stored in three structured layers:

Bronze Layer: Raw data as retrieved from the API.

Silver Layer: Cleaned and transformed data for analytics.

Gold Layer: Aggregated and ready-to-serve data for ad hoc queries.

Orchestration: The pipeline is scheduled to run daily at midnight using Azure Data Factory (ADF).

Storage: All data is stored in Azure Synapse Analytics, enabling efficient ad hoc querying and analysis.

Security: Connection strings and sensitive information are securely managed using Azure Key Vault. 🔐💡✅

Data Source 🌋🌍🌐

This project utilizes earthquake data from the Earthquake Catalog API based on the FDSN Event Web Service Specification. 🌍📊🌀

This API allows custom searches for earthquake information using various parameters, such as:

Time Range: Filter earthquakes by start and end times.

Magnitude Range: Retrieve earthquakes within specific magnitude thresholds.

Location: Define bounding boxes for geographical constraints.

Depth: Specify depth ranges for the earthquake data.

Contributors: Filter by contributing networks or agencies.

For automated applications, it is recommended to use the Real-time GeoJSON Feeds for enhanced performance and availability. However, this project demonstrates the capability of working with the detailed and customizable search parameters provided by the Earthquake Catalog API. 🌟🌐💾

Pipeline Architecture 🔄🎮🏋️‍♂️

Extract: 📊📥✨

Data is fetched from the Earthquake Catalog API.

The API’s customizable search parameters are used to retrieve earthquake events for the last day.

Transform: 🔄💻🛠

Data is cleaned and processed using Databricks.

Transformation steps include handling missing values, formatting data types, and aggregating key metrics.

Load: 📤📊🔧

Transformed data is loaded into Azure Synapse Analytics.

Data is organized into the Medallion Architecture:

Bronze Layer: Raw data.

Silver Layer: Processed and transformed data.

Gold Layer: Aggregated data ready for querying.

Orchestration: 🔄⏰📈

Azure Data Factory (ADF) is used to orchestrate and schedule the pipeline.

The pipeline runs automatically at midnight every day.

Security: 🔐⚙️💡

Secrets for API keys, database connection strings, and other sensitive information are securely managed using Azure Key Vault.

Tools & Technologies 🛠📊🎨

Azure Services: Azure Data Factory, Azure Synapse Analytics, Azure Key Vault 🎯📈🌟

Databricks: Data processing and transformation 🔄💻✨

Earthquake Catalog API: Data source for earthquake information 🌋🌍📊

Medallion Architecture: Bronze, Silver, and Gold layers for structured data storage 📂🔧📈

Scheduling: Daily orchestration using ADF 🔄⏰🌐
