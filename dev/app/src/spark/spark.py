from pyspark.sql import SparkSession   # type: ignore

def spark_session():
    return SparkSession.builder \
        .appName("DataCleaning") \
        .getOrCreate()