from spark.spark import spark_session

def set_statement_data(df_final):
    spark = spark_session()

    jdbc_url = "jdbc:postgresql://postgres:5432/mspr501"
    properties = {
        "user": "mspr501",
        "password": "s5t4v5",
        "driver": "org.postgresql.Driver"
    }

    df_final.write \
        .jdbc(url=jdbc_url, table="statement", mode="append", properties=properties)
    
    spark.stop()

    print(f"[INFO] Lignes insérées dans la table 'statement'.")