import os
from spark.spark import spark_session
from pyspark.sql.functions import udf, lit, col         # type: ignore
from pyspark.sql.types import IntegerType               # type: ignore

from db.connection import get_connection


def clean_covid():

    spark = spark_session()

    df = spark.read.csv("data_files/corona-virus-report/covid_19_clean_complete.csv", header=True, inferSchema=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_country, name FROM country")
    countries = {name: id_country for id_country, name in cursor.fetchall()}

    def get_country_id(name):
        return countries.get(name, None)

    get_country_id_udf = udf(get_country_id, IntegerType())

    df = df.withColumn("id_country", get_country_id_udf(col("Country/Region")))

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'covid'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df_final = df.select(
        col("Date").alias("_date"),
        col("Confirmed").cast(IntegerType()),
        col("Deaths").cast(IntegerType()),
        col("Recovered").cast(IntegerType()),
        col("Active").cast(IntegerType()),
        col("id_disease"),
        col("id_country")
    )

    cursor.close()
    conn.close()
    
    return df_final