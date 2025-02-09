import os
from pyspark.sql.functions import udf, lit, col     # type: ignore
from pyspark.sql import functions as F              # type: ignore
from pyspark.sql.types import IntegerType           # type: ignore

from db.connection import get_connection
from spark.spark import spark_session


def clean_sras():
    spark = spark_session()

    df = spark.read.csv("data_files/sars-outbreak-2003-complete-dataset/sars_2003_complete_dataset_clean.csv", header=True, inferSchema=True)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_country, name FROM country")
    countries = {name: id_country for id_country, name in cursor.fetchall()}

    def get_country_id(name):
        return countries.get(name, None)

    get_country_id_udf = udf(get_country_id, IntegerType())

    df = df.withColumn("id_country", get_country_id_udf(col("Country")))

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'sars'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df_aggregated = df.groupBy(
        col("date"), 
        col("id_country"), 
        col("id_disease")
    ).agg(
        F.sum("Cumulative number of case(s)").cast(IntegerType()).alias("Cumulative number of case(s)"),
        F.sum("Number of deaths").cast(IntegerType()).alias("Number of deaths"),
        F.sum("Number recovered").cast(IntegerType()).alias("Number recovered")
    )

    df_final = df_aggregated.select(
        col("Date").alias("_date"),
        col("`Cumulative number of case(s)`").alias("confirmed"),
        col("`Number of deaths`").alias("deaths"),
        col("`Number recovered`").alias("recovered"),
        col("id_disease"),
        col("id_country")
    )

    df_final = df_final.dropna()
    df_final = df_final.dropDuplicates()

    cursor.close()
    conn.close()

    return df_final