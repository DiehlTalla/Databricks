# Databricks notebook source
# MAGIC %md
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../Include/Copy-Datasets

# COMMAND ----------

# %python
files = dbutils.fs.ls(f"{dataset_bookstore}/customers-json")
display(files)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json/export_*.json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT count(*) FROM json.`${dataset.bookstore}/customers-json`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *,
# MAGIC    input_file_name() source_file
# MAGIC FROM json.`${dataset.bookstore}/customers-json`;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM text.`${dataset.bookstore}/customers-json`;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT *
# MAGIC FROM binaryFile.`${dataset.bookstore}/customers-json`;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM csv.`${dataset.bookstore}/books-csv`

# COMMAND ----------

external_location = "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/external_storage"

print(dataset_bookstore)  # vérifie la valeur d'abord

# COMMAND ----------

external_location = "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/external_storage"

dbutils.fs.cp(f"/Volumes/demoworkspace/default/bookstore_dataset/books-csv", f"{external_location}/books-csv", recurse=True)

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE books_csv
# MAGIC   (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
# MAGIC USING CSV
# MAGIC OPTIONS (header = "true", delimiter = ";")
# MAGIC LOCATION "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/external_storage/books-csv";

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM books_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE EXTENDED books_csv

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_bookstore}/books-csv")
display(files)

# COMMAND ----------

(spark.read
     .table("books_csv")
     .write
     .mode("append")
     .format("csv")
     .option("header", True)
     .option('delimiter', ';')
     .save(f"{dataset_bookstore}/books-csv"))

# COMMAND ----------

files = dbutils.fs.ls(f"{dataset_bookstore}/books-csv")
display(files)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM books_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC REFRESH TABLE books_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM books_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT(*) FROM books_csv

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE customers AS 
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json`;
# MAGIC
# MAGIC DESCRIBE EXTENDED customers;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE books_unparsed AS 
# MAGIC SELECT * FROM json.`${dataset.bookstore}/customers-json`;
# MAGIC
# MAGIC SELECT * FROM books_unparsed;
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP TABLE IF EXISTS books_tmp_vw;

# COMMAND ----------

# MAGIC %sql
# MAGIC
# MAGIC
# MAGIC CREATE TEMP VIEW books_tmp_vw
# MAGIC     (book_id STRING, book_title STRING, author STRING, price DOUBLE)
# MAGIC USING csv
# MAGIC OPTIONS (path =  "${dataset.bookstore}/books-csv/export_*.csv",
# MAGIC  header = "true", delimiter = ";");
# MAGIC CREATE TABLE books AS SELECT * FROM books_tmp_vw;
# MAGIC SELECT * FROM books

# COMMAND ----------


