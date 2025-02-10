import os
from utils.get_country_code_by_name import get_country_code_by_name as get_country_code
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

    cursor.execute("SELECT id_country, iso_code FROM country")
    countries = {iso_code: id_country for id_country, iso_code in cursor.fetchall()}

    def get_country_id(country_name):
        """Retourne l'id du pays si le code ISO2 est en base, sinon None"""
        iso_code = get_country_code(country_name)  # Conversion du nom en code ISO2
        return countries.get(iso_code, None)

    get_country_id_udf = udf(get_country_id, IntegerType())

    df = df.withColumn("id_country", get_country_id_udf(col("Country"))).dropna(subset=["id_country"])

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'h1n1'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df_final = df.select(
        col("Date").alias("_date"),
        col("`Cumulative no. of cases`").alias("Confirmed"),
        col("`Cumulative no. of deaths`").alias("Deaths"),
        col("id_disease"),
        col("id_country")
    ).dropna().dropDuplicates()

    cursor.close()
    conn.close()

    return df_final
