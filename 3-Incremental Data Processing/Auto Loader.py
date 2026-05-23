# Databricks notebook source
# MAGIC %md
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../Include/Copy-Datasets

# COMMAND ----------

print(dataset_bookstore)

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_bookstore}/orders-raw")
                      
display(files)

# COMMAND ----------

(spark.readStream
      .format("cloudFiles")
      .option("cloudFiles.format", "parquet")
      .option("cloudFiles.schemaLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_checkpoint")
      .load(f"{dataset_bookstore}/orders-raw")
      .writeStream
      .option("checkpointLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_checkpoint")
      .toTable("orders_updates")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM orders_updates

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM orders_updates

# COMMAND ----------

load_new_data()

# COMMAND ----------

load_new_data()

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_bookstore}/orders-raw")
display(files)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM orders_updates

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY orders_updates

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE  orders_updates

# COMMAND ----------

dbutils.fs.rm("abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/orders_checkpoint", True)

# COMMAND ----------


