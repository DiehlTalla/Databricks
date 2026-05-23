# Databricks notebook source
# MAGIC %md
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../Include/Copy-Datasets

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM oders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC    order_id,
# MAGIC    books,
# MAGIC    FILTER (books, i-> i.quantity >= 2) AS multiple_copies
# MAGIC FROM oders

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC    order_id,multiple_copies
# MAGIC FROM (
# MAGIC    SELECT
# MAGIC       order_id,   
# MAGIC    FILTER (books, i-> i.quantity >= 2) AS multiple_copies
# MAGIC FROM oders
# MAGIC ) WHERE size(multiple_copies) > 0

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT 
# MAGIC   order_id,
# MAGIC   books,
# MAGIC   TRANSFORM (
# MAGIC     books,
# MAGIC     b-> CAST(b.subtotal * 0.8 AS INT)
# MAGIC
# MAGIC   ) AS subtotal_after_discount
# MAGIC FROM oders;

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE FUNCTION get_url(email STRING)
# MAGIC RETURNS STRING
# MAGIC RETURN concat("http://www.", split(email, "@")[1])
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT email, get_url(email) domain
# MAGIC FROM customers

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE FUNCTION get_url

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE FUNCTION EXTENDED get_url

# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE FUNCTION site_type(email STRING)
# MAGIC RETURNS STRING
# MAGIC RETURN CASE 
# MAGIC          WHEN email LIKE "%.com" THEN "Commercial business"
# MAGIC          WHEN email LIKE "%.org" THEN "Non-profits organization"
# MAGIC          WHEN email LIKE "%.edu" THEN "Educational institution"
# MAGIC         ELSE concat("Unknown extenstion for education for domain: ", split(email, "@")[1])
# MAGIC        END;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT email, site_type(email) as domain_category
# MAGIC FROM customers
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC DROP FUNCTION get_url;
# MAGIC DROP FUNCTION site_type;

# COMMAND ----------


