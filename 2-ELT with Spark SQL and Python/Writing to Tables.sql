-- Databricks notebook source
-- MAGIC %md-sandbox
-- MAGIC
-- MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %run ../Include/Copy-Datasets

-- COMMAND ----------

CREATE TABLE oders AS SELECT * FROM parquet.`${dataset.bookstore}/orders`

-- COMMAND ----------

SELECT * FROM oders

-- COMMAND ----------

CREATE OR REPLACE TABLE oders AS SELECT * FROM parquet.`${dataset.bookstore}/orders`

-- COMMAND ----------

DESCRIBE HISTORY oders

-- COMMAND ----------

INSERT OVERWRITE oders SELECT * FROM parquet.`${dataset.bookstore}/orders`

-- COMMAND ----------

DESCRIBE HISTORY oders

-- COMMAND ----------

INSERT OVERWRITE oders SELECT *, current_timestamp() FROM parquet.`${dataset.bookstore}/orders`

-- COMMAND ----------

INSERT INTO  oders SELECT * FROM parquet.`${dataset.bookstore}/orders`

-- COMMAND ----------

SELECT COUNT (*) FROM oders

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW customer_updates AS SELECT * FROM json.`${dataset.bookstore}/customers-json-new`;
MERGE INTO customers c
USING customer_updates u
ON c.customer_id = u.customer_id
WHEN MATCHED AND c.email IS NULL AND  u.email IS NOT NULL 
THEN UPDATE SET email = u.email, updated = u.updated
WHEN NOT MATCHED THEN INSERT *

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW books_updates
    (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
    USING csv
    OPTIONS (
        path "${dataset.bookstore}/books-csv-new",
        header "true",
        delimiter = ";"
    );
    SELECT * FROM books_updates;

-- COMMAND ----------

MERGE INTO books b
USING books_updates u
ON b.book_id = u.book_id AND b.title = u.title
WHEN NOT MATCHED AND u.category = 'Computer Science' THEN
  INSERT *

-- COMMAND ----------


