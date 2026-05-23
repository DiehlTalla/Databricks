-- Databricks notebook source
-- MAGIC %md
-- MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
-- MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
-- MAGIC </div>

-- COMMAND ----------

-- MAGIC %run ../Include/Copy-Datasets

-- COMMAND ----------

SELECT * FROM customers

-- COMMAND ----------

DESCRIBE customers

-- COMMAND ----------

SELECT customer_id, profile:first_name, profile:adress:country 
FROM customers

-- COMMAND ----------

SELECT from_json(profile) AS profil_struct
FROM customers;

-- COMMAND ----------

SELECT profile
FROM customers 
LIMIT 1

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW parsed_customers AS 
   SELECT customer_id, from_json(profile, schema_of_json('{"first_name":"Susana","last_name":"Gonnely","gender":"Female","address":{"street":"760 Express Court","city":"Obrenovac","country":"Serbia"}}')) AS profile_struct
   FROM customers ;
   SELECT* FROM parsed_customers

-- COMMAND ----------

DESCRIBE parsed_customers

-- COMMAND ----------

SELECT customer_id, profile_struct.first_name, profile_struct.address.country
FROM parsed_customers

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW customers_final AS 
SELECT customer_id, profile_struct.*
FROM parsed_customers;

SELECT * FROM customers_final

-- COMMAND ----------

SELECT order_id, customer_id, books
FROM oders

-- COMMAND ----------

SELECT order_id,explode(books) AS book
FROM oders

-- COMMAND ----------

SELECT customer_id,
  collect_set(order_id) AS orders_set,
  collect_set(books.book_id) AS books_set
FROM oders
GROUP BY customer_id

-- COMMAND ----------

SELECT customer_id,
  collect_set(books.book_id) AS before_flatten,
  array_distinct(flatten(collect_set(books.book_id))) AS after_flatten
  FROM oders
  GROUP BY customer_id

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW orders_enriched AS 
SELECT *
FROM(
    SELECT *, explode(books) AS book
    FROM oders) o 
INNER JOIN books_csv b 
ON o.book.book_id = b.book_id;
SELECT *
FROM orders_enriched

-- COMMAND ----------

CREATE OR REPLACE TEMP VIEW orders_updates 
AS SELECT * FROM parquet.`${dataset.bookstore}/orders-new`;

SELECT * FROM oders
UNION
SELECT * FROM orders_updates

-- COMMAND ----------

SELECT * FROM oders
INTERSECT
SELECT * FROM orders_update

-- COMMAND ----------

CREATE OR REPLACE TABLE transactions AS 
SELECT * FROM (
    SELECT
       customer_id,
       book.book_id AS book_id,
       book.quantity AS quantity
    FROM orders_enriched 
)PIVOT ( 
 sum(quantity) FOR book_id in (
    'BO1', 'BO2', 'BO3', 'BO4', 'BO5', 'BO6', 
    'BO7', 'BO8', 'BO9', 'BO10', 'BO11', 'BO12'
 )   
) ;
SELECT * FROM transactions

-- COMMAND ----------

SHOW TABLES IN  demoworkspace.default

-- COMMAND ----------


