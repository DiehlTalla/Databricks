# Databricks notebook source
# MAGIC %md
# MAGIC %md
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../Include/Copy-Datasets

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_bookstore}/orders-raw")
display(files)

# COMMAND ----------

(spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "parquet")
      .option("cloudFiles.schemaLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_checkpoint")
      .load(f"{dataset_bookstore}/orders-raw")
      .createOrReplaceTempView("orders_raw_temp"))
     

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW oders_tmp AS (
# MAGIC     SELECT *, current_timestamp() arrival_time, input_file_name() source_file
# MAGIC     FROM orders_raw_temp
# MAGIC )

# COMMAND ----------

import time

orders_tmp_df = spark.sql("SELECT * FROM oders_tmp")
display(orders_tmp_df, checkpointLocation = "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/tmp/orders_" + str(time.time()))

# COMMAND ----------

(spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "parquet")
      .option("cloudFiles.schemaLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_schema")
      .load(f"{dataset_bookstore}/orders-raw")
      .writeStream
      .format("delta")
      .option("checkpointLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_checkpoint")
      .outputMode("append")
      .table("orders_bronze")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM orders_bronze

# COMMAND ----------

load_new_data()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM orders_bronze

# COMMAND ----------

load_new_data()

# COMMAND ----------

(spark.read
      .format("json")
      .load(f"{dataset_bookstore}/customers-json")
      .createOrReplaceTempView("customers_lookup"))
      

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers_lookup

# COMMAND ----------

(spark.readStream
      .table("orders_bronze")
      .createOrReplaceTempView("orders_bronze_tmp"))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMPORARY VIEW orders_enriched_tmp AS (
# MAGIC     SELECT order_id, quantity, o.customer_id, c.profile:first_name as f_name, c.profile:last_name as l_name, cast(from_unixtime(order_timestamp, 'yyyy-MM-dd HH:mm:ss') as timestamp) as order_timestamp, books
# MAGIC     FROM orders_bronze_tmp o
# MAGIC     INNER JOIN customers_lookup c
# MAGIC     ON o.customer_id = c.customer_id
# MAGIC     WHERE quantity > 0)
# MAGIC

# COMMAND ----------

(spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "parquet")
      .option("cloudFiles.schemaLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_schema")
      .load(f"{dataset_bookstore}/orders-raw")
      .writeStream
      .format("delta")
      .option("checkpointLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_checkpoint2")
      .outputMode("append")
      .table("orders_silvers")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM orders_silvers

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED orders_silvers
# MAGIC

# COMMAND ----------

for stream in spark.streams.active:
    print(stream.name, stream.status)

# COMMAND ----------

dbutils.fs.ls(f"{dataset_bookstore}/orders-raw")

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM orders_silvers

# COMMAND ----------

load_new_data()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM orders_silvers

# COMMAND ----------

(spark.readStream
      .table("orders_silvers")
      .createOrReplaceTempView("orders_silvers_tmp"))

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW daily_customer_books_tmp AS (
# MAGIC     SELECT o.customer_id, c.f_name, c.l_name, date_trunc("DD", o.order_timestamp) order_date, sum(o.quantity) books_counts
# MAGIC     FROM orders_silvers_tmp o 
# MAGIC     INNER JOIN customer c
# MAGIC     ON o.customer_id = c.customer_id
# MAGIC     GROUP BY o.customer_id, c.f_name, c.l_name,date_trunc("DD", o.order_timestamp)
# MAGIC     )

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE customers

# COMMAND ----------

for s in spark.streams.active:
    print("stopping stream: " +s.id)
    s.stop()
    s.awaitTermination()

# COMMAND ----------


