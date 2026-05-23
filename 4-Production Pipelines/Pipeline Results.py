# Databricks notebook source
files = dbutils.fs.ls("/Volumes/demoworkspace/default/bookstore_dataset")
display(files)

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN demoworkspace.default;

# COMMAND ----------



# COMMAND ----------


