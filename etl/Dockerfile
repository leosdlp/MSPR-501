FROM openjdk:11-jdk-slim

# Installer Python, pip, curl, et les bibliothèques nécessaires (PySpark, Matplotlib, et Requests)
RUN apt-get update && apt-get install -y python3 python3-pip curl && \
    pip3 install pyspark matplotlib requests && \
    apt-get clean

# Télécharger Spark
RUN curl -O https://dlcdn.apache.org/spark/spark-3.4.4/spark-3.4.4-bin-hadoop3.tgz && \
    tar -xvf spark-3.4.4-bin-hadoop3.tgz -C /opt/ && \
    rm spark-3.4.4-bin-hadoop3.tgz

# Configurer Spark
ENV SPARK_HOME=/opt/spark-3.4.4-bin-hadoop3
ENV PATH="$SPARK_HOME/bin:$PATH"

WORKDIR /app
COPY . .

CMD ["python3", "script_etl.py"]
