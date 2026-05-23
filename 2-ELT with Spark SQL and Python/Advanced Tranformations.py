# Databricks notebook source
# MAGIC %md
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../Include/Copy-Datasets

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM customers
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE customers
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id, profile:first_name, profile:adress:country 
# MAGIC FROM customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT from_json(profile) AS profil_struct
# MAGIC FROM customers;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT profile
# MAGIC FROM customers 
# MAGIC LIMIT 1

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW parsed_customers AS 
# MAGIC    SELECT customer_id, from_json(profile, schema_of_json('{"first_name":"Susana","last_name":"Gonnely","gender":"Female","address":{"street":"760 Express Court","city":"Obrenovac","country":"Serbia"}}')) AS profile_struct
# MAGIC    FROM customers ;
# MAGIC    SELECT* FROM parsed_customers
# MAGIC
# MAGIC
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE parsed_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id, profile_struct.first_name, profile_struct.address.country
# MAGIC FROM parsed_customers

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW customers_final AS 
# MAGIC SELECT customer_id, profile_struct.*
# MAGIC FROM parsed_customers;
# MAGIC
# MAGIC SELECT * FROM customers_final

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id, customer_id, books
# MAGIC FROM oders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT order_id,explode(books) AS book
# MAGIC FROM oders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id,
# MAGIC   collect_set(order_id) AS orders_set,
# MAGIC   collect_set(books.book_id) AS books_set
# MAGIC FROM oders
# MAGIC GROUP BY customer_id

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT customer_id,
# MAGIC   collect_set(books.book_id) AS before_flatten,
# MAGIC   array_distinct(flatten(collect_set(books.book_id))) AS after_flatten
# MAGIC   FROM oders
# MAGIC   GROUP BY customer_id

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW orders_enriched AS 
# MAGIC SELECT *
# MAGIC FROM(
# MAGIC     SELECT *, explode(books) AS book
# MAGIC     FROM oders) o 
# MAGIC INNER JOIN books_csv b 
# MAGIC ON o.book.book_id = b.book_id;
# MAGIC SELECT *
# MAGIC FROM orders_enriched    

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW orders_updates 
# MAGIC AS SELECT * FROM parquet.`${dataset.bookstore}/orders-new`;
# MAGIC
# MAGIC SELECT * FROM oders
# MAGIC UNION
# MAGIC SELECT * FROM orders_updates
# MAGIC
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM oders
# MAGIC INTERSECT
# MAGIC SELECT * FROM orders_update

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TABLE transactions AS 
# MAGIC SELECT * FROM (
# MAGIC     SELECT
# MAGIC        customer_id,
# MAGIC        book.book_id AS book_id,
# MAGIC        book.quantity AS quantity
# MAGIC     FROM orders_enriched 
# MAGIC )PIVOT ( 
# MAGIC  sum(quantity) FOR book_id in (
# MAGIC     'BO1', 'BO2', 'BO3', 'BO4', 'BO5', 'BO6', 
# MAGIC     'BO7', 'BO8', 'BO9', 'BO10', 'BO11', 'BO12'
# MAGIC  )   
# MAGIC ) ;
# MAGIC SELECT * FROM transactions
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SHOW TABLES IN  demoworkspace.default 

# COMMAND ----------


