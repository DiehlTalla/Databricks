-- Databricks notebook source
-- MAGIC %md
-- MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %run ../Include/Copy-Datasets

-- COMMAND ----------

-- MAGIC %python
-- MAGIC # %python
-- MAGIC files = dbutils.fs.ls(f"{dataset_bookstore}/customers-json")
-- MAGIC display(files)

-- COMMAND ----------

SELECT * FROM json.`${dataset.bookstore}/customers-json/export_*.json`

-- COMMAND ----------

SELECT * FROM json.`${dataset.bookstore}/customers-json`

-- COMMAND ----------

SELECT count(*) FROM json.`${dataset.bookstore}/customers-json`

-- COMMAND ----------

SELECT *,
   input_file_name() source_file
FROM json.`${dataset.bookstore}/customers-json`;

-- COMMAND ----------

SELECT *
FROM text.`${dataset.bookstore}/customers-json`;

-- COMMAND ----------

SELECT *
FROM binaryFile.`${dataset.bookstore}/customers-json`;

-- COMMAND ----------

SELECT * FROM csv.`${dataset.bookstore}/books-csv`

-- COMMAND ----------

-- MAGIC %python
-- MAGIC external_location = "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/external_storage"
-- MAGIC
-- MAGIC print(dataset_bookstore)  # vérifie la valeur d'abord

-- COMMAND ----------

-- MAGIC %python
-- MAGIC external_location = "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/external_storage"
-- MAGIC
-- MAGIC dbutils.fs.cp(f"/Volumes/demoworkspace/default/bookstore_dataset/books-csv", f"{external_location}/books-csv", recurse=True)

-- COMMAND ----------

CREATE TABLE books_csv
  (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
USING CSV
OPTIONS (header = "true", delimiter = ";")
LOCATION "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/external_storage/books-csv";

-- COMMAND ----------

SELECT * FROM books_csv

-- COMMAND ----------

DESCRIBE EXTENDED books_csv

-- COMMAND ----------

-- MAGIC %python
-- MAGIC files = dbutils.fs.ls(f"{dataset_bookstore}/books-csv")
-- MAGIC display(files)

-- COMMAND ----------

-- MAGIC %python
-- MAGIC (spark.read
-- MAGIC      .table("books_csv")
-- MAGIC      .write
-- MAGIC      .mode("append")
-- MAGIC      .format("csv")
-- MAGIC      .option("header", True)
-- MAGIC      .option('delimiter', ';')
-- MAGIC      .save(f"{dataset_bookstore}/books-csv"))
-- MAGIC        
-- MAGIC

-- COMMAND ----------

-- MAGIC %python
-- MAGIC files = dbutils.fs.ls(f"{dataset_bookstore}/books-csv")
-- MAGIC display(files)

-- COMMAND ----------

SELECT COUNT(*) FROM books_csv

-- COMMAND ----------

REFRESH TABLE books_csv

-- COMMAND ----------

SELECT COUNT(*) FROM books_csv

-- COMMAND ----------

SELECT COUNT(*) FROM books_csv

-- COMMAND ----------

CREATE TABLE customers AS 
SELECT * FROM json.`${dataset.bookstore}/customers-json`;

DESCRIBE EXTENDED customers;

-- COMMAND ----------

CREATE TABLE books_unparsed AS 
SELECT * FROM json.`${dataset.bookstore}/customers-json`;

SELECT * FROM books_unparsed;

-- COMMAND ----------

DROP TABLE IF EXISTS books_tmp_vw;

-- COMMAND ----------



CREATE TEMP VIEW books_tmp_vw
    (book_id STRING, book_title STRING, author STRING, price DOUBLE)
USING csv
OPTIONS (path =  "${dataset.bookstore}/books-csv/export_*.csv",
 header = "true", delimiter = ";");
CREATE TABLE books AS SELECT * FROM books_tmp_vw;
SELECT * FROM books

-- COMMAND ----------


