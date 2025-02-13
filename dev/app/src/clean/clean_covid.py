"""
Module de nettoyage et d'agrégation des données COVID-19.

Ce module utilise PySpark pour lire et transformer un fichier CSV contenant les données COVID-19,
les enrichit avec des informations issues d'une base de données, et retourne un DataFrame PySpark
agrégé prêt pour insertion ou analyse.

Optimisations :
- Utilisation d'un schéma explicite pour éviter l'inférence automatique
- Récupération optimisée des données pays et maladie depuis la base
- Remplacement de l'UDF par une transformation RDD plus performante
- Ajout de `dropDuplicates()` pour éviter les doublons
- Suppression des valeurs nulles après l'agrégation

Dépendances :
- PySpark
- Une base de données contenant les informations de pays et de maladies.
- Une fonction utilitaire pour convertir un nom de pays en code ISO.
"""

from pyspark.sql.functions import col, lit, sum as F_sum                        # type: ignore
from pyspark.sql.types import IntegerType, StringType, StructType, StructField  # type: ignore
from db.connection import get_connection
from spark.spark import spark_session

def clean_covid():
    spark = spark_session()

    schema = StructType([
        StructField("Date", StringType(), True),
        StructField("Country/Region", StringType(), True),
        StructField("Confirmed", IntegerType(), True),
        StructField("Deaths", IntegerType(), True),
        StructField("Recovered", IntegerType(), True),
        StructField("Active", IntegerType(), True)
    ])

    df = spark.read.csv(
        "data_files/corona-virus-report/covid_19_clean_complete.csv",
        header=True,
        schema=schema
    )

    df = df.repartition(6)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT id_country, name FROM country")
    countries_list = cursor.fetchall()
    countries_dict = {name: id_country for id_country, name in countries_list}

    df = df.rdd.map(lambda row: row + (countries_dict.get(row[1], None),)).toDF(
        df.schema.add("id_country", IntegerType())
    )

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'covid'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df_aggregated = df.groupBy(
        col("Date"),
        col("id_country"),
        col("id_disease")
    ).agg(
        F_sum("Confirmed").cast(IntegerType()).alias("Confirmed"),
        F_sum("Deaths").cast(IntegerType()).alias("Deaths"),
        F_sum("Recovered").cast(IntegerType()).alias("Recovered"),
        F_sum("Active").cast(IntegerType()).alias("Active")
    )

    df_final = df_aggregated.select(
        col("Date").alias("_date"),
        col("Confirmed"),
        col("Deaths"),
        col("Recovered"),
        col("Active"),
        col("id_disease"),
        col("id_country")
    ).dropna().dropDuplicates()

    cursor.close()
    conn.close()

    return df_final