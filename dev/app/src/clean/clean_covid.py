"""
Module de nettoyage et d'agrégation des données COVID-19.

Ce module utilise PySpark pour lire et transformer un fichier CSV contenant les données COVID-19, 
les enrichit avec des informations issues d'une base de données, et retourne un DataFrame PySpark 
agrégé prêt pour insertion ou analyse.

Fonctionnalités principales :
- Lecture et transformation des données à l'aide de PySpark.
- Enrichissement avec des données pays et maladie depuis une base de données.
- Agrégation des données par date, pays et maladie.

Dépendances :
- PySpark
- Une base de données contenant les informations de pays et de maladies.
- Une fonction utilitaire pour convertir un nom de pays en code ISO.

"""

from pyspark.sql.functions import col, udf, lit, sum as F_sum   # type: ignore
from pyspark.sql.types import IntegerType                       # type: ignore
from pyspark.sql.types import StringType                        # type: ignore

from utils.get_country_code_by_name import get_country_code_by_name as get_country_code
from db.connection import get_connection
from spark.spark import spark_session


def clean_covid():
    """
    Nettoie et agrège les données COVID-19.

    Cette fonction lit un fichier CSV contenant les données COVID-19, les enrichit avec des informations 
    issues d'une base de données (codes ISO des pays et ID de la maladie), et agrège les données par 
    date, pays et maladie. 

    Étapes principales :
    1. Lecture du fichier CSV contenant les données brutes COVID-19.
    2. Récupération des codes ISO des pays et des identifiants de maladie depuis une base de données.
    3. Ajout des codes ISO aux données COVID-19 via une jointure.
    4. Sélection des colonnes pertinentes et suppression des lignes avec des valeurs nulles.
    5. Agrégation des données par date, pays et maladie.

    Returns:
        pyspark.sql.DataFrame: Un DataFrame PySpark contenant les données agrégées avec les colonnes suivantes :
            - `_date` : Date des données agrégées.
            - `id_country` : Identifiant du pays.
            - `id_disease` : Identifiant de la maladie.
            - `Confirmed` : Nombre total de cas confirmés.
            - `Deaths` : Nombre total de décès.
            - `Recovered` : Nombre total de cas récupérés.
            - `Active` : Nombre total de cas actifs.
    """
    spark = spark_session()

    df = spark.read.csv(
        "data_files/corona-virus-report/covid_19_clean_complete.csv",
        header=True,
        inferSchema=True
    )

    df = df.repartition(6)
    print(df.rdd.getNumPartitions())

    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_country, iso_code FROM country")
    countries = {iso_code: id_country for id_country, iso_code in cursor.fetchall()}

    countries_data = [(id_country, iso_code) for iso_code, id_country in countries.items()]
    countries_columns = ["id_country", "iso_code"]
    countries_df = spark.createDataFrame(countries_data, countries_columns)

    @udf(StringType())
    def get_country_code_udf(country_name):
        return get_country_code(country_name) if country_name else None

    df = df.withColumn("iso_code", get_country_code_udf(col("`Country/Region`")))

    df = df.join(
        countries_df,
        df["iso_code"] == countries_df["iso_code"],
        how="left"
    ).drop("iso_code")

    cursor.execute("SELECT id_disease FROM disease WHERE name = 'covid'")
    id_disease = cursor.fetchone()[0]

    df = df.withColumn("id_disease", lit(id_disease).cast(IntegerType()))

    df = df.select(
        col("Date").alias("_date"),
        col("Confirmed").cast(IntegerType()),
        col("Deaths").cast(IntegerType()),
        col("Recovered").cast(IntegerType()),
        col("Active").cast(IntegerType()),
        col("id_disease"),
        col("id_country")
    ).dropna()

    df_aggregated = df.groupBy(
        "_date", "id_country", "id_disease"
    ).agg(
        F_sum("Confirmed").alias("Confirmed"),
        F_sum("Deaths").alias("Deaths"),
        F_sum("Recovered").alias("Recovered"),
        F_sum("Active").alias("Active")
    )

    cursor.close()
    conn.close()

    return df_aggregated
