import os
from pyspark.sql.functions import udf, lit, col     # type: ignore
from pyspark.sql import functions as F              # type: ignore
from pyspark.sql.types import IntegerType           # type: ignore

from db.connection import get_connection
from spark.spark import spark_session


def clean_h1n1():
    spark = spark_session()

    df = spark.read.csv("data_files/h1n1-swine-flu-2009-pandemic-dataset/data.csv", header=True, inferSchema=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_country, name FROM country")
    countries = {name: id_country for id_country, name in cursor.fetchall()}

    def get_country_id(name):
        return countries.get(name, None)

    get_country_id_udf = udf(get_country_id, IntegerType())

    df = df.withColumn("id_country", get_country_id_udf(col("Country")))

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'h1n1'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    #df_aggregated = df.groupBy(
    #    col("Date"), 
    #    col("id_country"), 
    #    col("id_disease")
    #).agg(
    #    F.sum("Cumulative no. of cases").cast(IntegerType()).alias("Cumulative no. of cases"),
    #    F.sum("Cumulative no. of deaths").cast(IntegerType()).alias("Cumulative no. of deaths"),
    #)

    df_final = df.select(
        col("Date").alias("_date"),
        col("`Cumulative no. of cases`").alias("Confirmed"),
        col("`Cumulative no. of deaths`").alias("Deaths"),
        col("id_disease"),
        col("id_country")
    )

    df_final = df_final.dropna()
    df_final = df_final.dropDuplicates()

    cursor.close()
    conn.close()

    return df_final