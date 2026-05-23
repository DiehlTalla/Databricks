-- Databricks notebook source
-- MAGIC %md
-- MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %run ../Include/Copy-Datasets

-- COMMAND ----------

SELECT * FROM oders

-- COMMAND ----------

SELECT
   order_id,
   books,
   FILTER (books, i-> i.quantity >= 2) AS multiple_copies
FROM oders

-- COMMAND ----------

SELECT
   order_id,multiple_copies
FROM (
   SELECT
      order_id,   
   FILTER (books, i-> i.quantity >= 2) AS multiple_copies
FROM oders
) WHERE size(multiple_copies) > 0

-- COMMAND ----------

SELECT 
  order_id,
  books,
  TRANSFORM (
    books,
    b-> CAST(b.subtotal * 0.8 AS INT)

  ) AS subtotal_after_discount
FROM oders;

-- COMMAND ----------

CREATE OR REPLACE FUNCTION get_url(email STRING)
RETURNS STRING
RETURN concat("http://www.", split(email, "@")[1])

-- COMMAND ----------

SELECT email, get_url(email) domain
FROM customers

-- COMMAND ----------

DESCRIBE FUNCTION get_url

-- COMMAND ----------

DESCRIBE FUNCTION EXTENDED get_url

-- COMMAND ----------

CREATE FUNCTION site_type(email STRING)
RETURNS STRING
RETURN CASE 
         WHEN email LIKE "%.com" THEN "Commercial business"
         WHEN email LIKE "%.org" THEN "Non-profits organization"
         WHEN email LIKE "%.edu" THEN "Educational institution"
        ELSE concat("Unknown extenstion for education for domain: ", split(email, "@")[1])
       END;

-- COMMAND ----------

SELECT email, site_type(email) as domain_category
FROM customers

-- COMMAND ----------

DROP FUNCTION get_url;
DROP FUNCTION site_type;

-- COMMAND ----------


