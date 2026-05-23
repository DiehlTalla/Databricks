# Databricks notebook source
# MAGIC %md-sandbox
# MAGIC
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../Include/Copy-Datasets

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE TABLE oders AS SELECT * FROM parquet.`${dataset.bookstore}/orders`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM oders

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE oders AS SELECT * FROM parquet.`${dataset.bookstore}/orders`

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY oders

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT OVERWRITE oders SELECT * FROM parquet.`${dataset.bookstore}/orders`

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE HISTORY oders

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT OVERWRITE oders SELECT *, current_timestamp() FROM parquet.`${dataset.bookstore}/orders`

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO  oders SELECT * FROM parquet.`${dataset.bookstore}/orders`

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT COUNT (*) FROM oders

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW customer_updates AS SELECT * FROM json.`${dataset.bookstore}/customers-json-new`;
# MAGIC MERGE INTO customers c
# MAGIC USING customer_updates u
# MAGIC ON c.customer_id = u.customer_id
# MAGIC WHEN MATCHED AND c.email IS NULL AND  u.email IS NOT NULL 
# MAGIC THEN UPDATE SET email = u.email, updated = u.updated
# MAGIC WHEN NOT MATCHED THEN INSERT *
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW books_updates
# MAGIC     (book_id STRING, title STRING, author STRING, category STRING, price DOUBLE)
# MAGIC     USING csv
# MAGIC     OPTIONS (
# MAGIC         path "${dataset.bookstore}/books-csv-new",
# MAGIC         header "true",
# MAGIC         delimiter = ";"
# MAGIC     );
# MAGIC     SELECT * FROM books_updates;

# COMMAND ----------

# MAGIC %sql
# MAGIC MERGE INTO books b
# MAGIC USING books_updates u
# MAGIC ON b.book_id = u.book_id AND b.title = u.title
# MAGIC WHEN NOT MATCHED AND u.category = 'Computer Science' THEN
# MAGIC   INSERT *

# COMMAND ----------


