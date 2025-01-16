FROM python:3.11-slim

WORKDIR /app

RUN apt-get update && apt-get install -y --no-install-recommends \
    git \
    libpq-dev gcc \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir flask gunicorn psycopg2-binary

EXPOSE 5000

CMD git clone https://github.com/Enzobu/api-mspr501.git . && pip install --no-cache-dir -r requirements.txt && gunicorn -w 4 -b 0.0.0.0:5000 app:app