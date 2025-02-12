"""
Module de nettoyage des données pour l'épidémie de SRAS (2003).

Ce module utilise PySpark pour nettoyer et transformer les données brutes concernant l'épidémie de SRAS en 2003.
Les données sont enrichies avec des informations sur les pays, associées à l'identifiant de la maladie, 
et agrégées par date, pays et maladie avant d'être prêtes à être insérées dans une base de données.

Fonctionnalités principales :
- Chargement et partitionnement des données brutes.
- Enrichissement des données avec des identifiants de pays issus d'une base de données.
- Association des données à l'identifiant de la maladie.
- Agrégation des cas confirmés, décès et guérisons.
- Gestion des valeurs manquantes et transformation des colonnes.

Dépendances :
- PySpark pour le traitement et l'agrégation des données.
- Une base de données pour récupérer les informations sur les pays et les maladies.
- Un fichier CSV contenant les données brutes sur le SRAS.

"""

from pyspark.sql.functions import udf, lit, col, sum as F_sum   # type: ignore
from pyspark.sql.types import IntegerType                       # type: ignore
from pyspark.sql.types import StringType                        # type: ignore

from db.connection import get_connection
from spark.spark import spark_session


def clean_sras():
    """
    Nettoie et transforme les données brutes sur le SRAS (2003).

    Cette fonction effectue les opérations suivantes :
    1. Chargement des données brutes depuis un fichier CSV.
    2. Partitionnement des données pour optimiser leur traitement avec PySpark.
    3. Enrichissement des données avec les identifiants des pays via une base de données.
    4. Association des données à l'identifiant de la maladie SRAS.
    5. Agrégation des cas confirmés, des décès et des guérisons par date, pays et maladie.
    6. Gestion des valeurs manquantes et suppression des colonnes inutiles.

    Returns:
        pyspark.sql.DataFrame: Un DataFrame PySpark contenant les données nettoyées, enrichies et agrégées, 
        prêtes pour l'insertion dans une base de données.

    Exceptions:
        Lève des erreurs en cas de problème avec la connexion à la base de données ou le traitement des
        données.
    """
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