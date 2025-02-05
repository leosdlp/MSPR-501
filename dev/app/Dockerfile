FROM openjdk:11-jdk-slim

RUN apt-get update && apt-get install -y --no-install-recommends \
    python3 \
    python3-pip \
    curl \
    libpq-dev \
    nano

RUN pip3 install pyspark  \
    matplotlib  \
    requests \
    pandas \
    dash \
    psycopg2-binary \
    python-dotenv && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

RUN curl -O https://downloads.apache.org/spark/spark-3.4.4/spark-3.4.4-bin-hadoop3.tgz && \
    tar -xvf spark-3.4.4-bin-hadoop3.tgz -C /opt/ && \
    rm spark-3.4.4-bin-hadoop3.tgz

WORKDIR /app

RUN echo "alias ll='ls -al'" >> /root/.bashrc && \
    echo "export PATH=$PATH:/app/bin/" >> /root/.bashrc

ENV SPARK_HOME=/opt/spark-3.4.4-bin-hadoop3
ENV PATH="$SPARK_HOME/bin:$PATH"
ENV PYTHONPATH=/app

CMD ["tail", "-f", "/dev/null"]

