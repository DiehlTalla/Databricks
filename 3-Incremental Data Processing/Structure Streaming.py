# Databricks notebook source
# MAGIC %md
# MAGIC <div  style="text-align: center; line-height: 0; padding-top: 9px;">
# MAGIC   <img src="https://raw.githubusercontent.com/derar-alhussein/Databricks-Certified-Data-Engineer-Associate/main/Includes/images/bookstore_schema.png" alt="Databricks Learning" style="width: 600">
# MAGIC </div>

# COMMAND ----------

# MAGIC %run ../Include/Copy-Datasets

# COMMAND ----------

(spark.readStream
      .table("books_csv")
      .createOrReplaceTempView("books_streaming_tmp_vw")
)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM books_streaming_tmp_vw
# MAGIC

# COMMAND ----------

(spark.readStream
      .table("books_csv")
      .writeStream
      .format("memory")
      .queryName("books_streaming_tmp_vw")
      .option("checkpointLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/books_streaming")
      .start()

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM books_streaming_tmp_vw

# COMMAND ----------

df = spark.sql("""
    SELECT author, count(book_id) AS total_books
    FROM books_streaming_tmp_vw
    GROUP BY author
""")

display(df, checkpointLocation = "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/books_streaming_agg")

# COMMAND ----------

df = spark.sql("""
    SELECT *
    FROM books_streaming_tmp_vw
    ORDER BY author
""")

display(df)


# COMMAND ----------

# MAGIC %sql
# MAGIC CREATE OR REPLACE TEMP VIEW author_counts_tmp_vw AS (
# MAGIC     SELECT author, count(book_id) AS total_books
# MAGIC     FROM books_streaming_tmp_vw
# MAGIC     GROUP BY author
# MAGIC )

# COMMAND ----------

(spark.table("author_counts_tmp_vw")
      .writeStream
      .trigger(processingTime='4 seconds')
      .outputMode("complete")
      .option("checkpointLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/author_counts")
      .table("author_counts")
)


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM author_counts

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO books_csv 
# MAGIC values ("B19", "Introduction to Modeling and Simulation", "Mark W. Spong", "Computer Science", 25),
# MAGIC         ("B20", "Robot Modeling and Control", "Mark W. Spong", "Computer Science", 30),
# MAGIC         ("B21", "Turing's Vision: The Birth of Computer Science", "Chris Bernhardt", "Computer Science", 35)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM author_counts
# MAGIC

# COMMAND ----------

# MAGIC %sql
# MAGIC INSERT INTO books_csv 
# MAGIC values ("B16", "Hands-On Deep Learning Algorithms with Python", "Sudharsan Ravichandiran", "Computer Science", 25),
# MAGIC         ("B17", "Neural Network Methods in Natural Language Processing", "Yoav Goldberg", "Computer Science", 30),
# MAGIC         ("B18", "Understanding digital signal processing", "Richard Lyons", "Computer Science", 35)

# COMMAND ----------

(spark.table("author_counts_tmp_vw")
      .writeStream
      .trigger(availableNow=True)
      .outputMode("complete")
      .option("checkpointLocation", "abfss://unity-catalog-storage@dbstorageb5xzbjmlfqwie.dfs.core.windows.net/7405611205197801/checkpoints/author_counts")
      .table("author_counts")
      .awaitTermination()
)


# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM author_counts

# COMMAND ----------


