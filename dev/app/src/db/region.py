from pyspark.sql import SparkSession        # type: ignore
from pyspark.sql.functions import col       # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


def get_region():
    spark = SparkSession.builder \
        .appName("JSON to DataFrame") \
        .getOrCreate()
    
    json_file_path = "./json/pays_region.json"
    df = spark.read.option("multiline", "true").json(json_file_path)

    regions_list = []

    for country in df.columns:
        country_region = df.select(col(country).getItem("region").alias("region"))
        regions_list.append(country_region)

    regions_df = regions_list[0]
    for region in regions_list[1:]:
        regions_df = regions_df.union(region)

    regions_df = regions_df.dropDuplicates()

    regions_list = [row["region"] for row in regions_df.collect() if row["region"]]

    spark.stop()

    return regions_list


def set_region():
    conn = get_connection()
    cursor = conn.cursor()

    truncate_table("region")

    regions_list = get_region()

    for region in regions_list:
        cursor.execute("""
            INSERT INTO region (name) 
            VALUES (%s) 
        """, (region,))
        print(f"[INFO] Région insérée : {region}")

    conn.commit()
    cursor.close()
    conn.close()

if __name__ == "__main__":
    set_region()