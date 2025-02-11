import os
from pyspark.sql.functions import col, udf, lit, sum as F_sum   # type: ignore
from pyspark.sql import functions as F                          # type: ignore
from pyspark.sql.types import IntegerType                       # type: ignore
from utils.get_country_code_by_name import get_country_code_by_name as get_country_code
from db.connection import get_connection
from spark.spark import spark_session
from pyspark.sql.types import StringType # type: ignore

def clean_covid():
    spark = spark_session()

    df = spark.read.csv(
            "data_files/corona-virus-report/covid_19_clean_complete.csv",
            header=True,
            inferSchema=True
        )
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
    df = df.drop("Province/State").drop("Lat").drop("Long").drop("Lat").drop("WHO Region")

    # df = df.dropna()

    print(df.count())
    # df_final = df.select(
    #     col("Date").alias("_date"),
    #     col("Confirmed"),
    #     col("Deaths"),
    #     col("Recovered"),
    #     col("Active"),
    #     col("id_disease"),
    #     col("id_country")
    # )

    # df_final.printSchema()


    
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


    

    cursor.close()
    conn.close()

    # return df_final
