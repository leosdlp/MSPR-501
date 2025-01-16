import os
import requests
import pandas as pd
import time
import psycopg2
from psycopg2.extras import execute_batch
from datetime import datetime

# Configurations PostgreSQL
DB_CONFIG = {
    "dbname": "mspr501",
    "user": "mspr501",
    "password": "s5t4v5",
    "host": "postgres",
    "port": 5432
}

time.sleep(10)

# URLs des fichiers CSV
file_urls = {
    "covid_summary": "https://lab.enzo-palermo.com/mspr501/data/mondial-covid-19/worldometer_coronavirus_summary_data.csv",
    "h1n1": "https://lab.enzo-palermo.com/mspr501/data/h1n1/data.csv",
    "sars": "https://lab.enzo-palermo.com/mspr501/data/sars_2003/sars_2003_complete_dataset_clean.csv",
    "monkeypox": "https://lab.enzo-palermo.com/mspr501/data/variole-du-singe/owid-monkeypox-data.csv"
}

# Téléchargement des fichiers
def download_file(name, url, download_dir="data_files"):
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, f"{name}.csv")
    if not os.path.exists(file_path):
        print(f"Téléchargement de {name} depuis {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Fichier {name} téléchargé avec succès.")
        else:
            raise Exception(f"Erreur lors du téléchargement de {name}: {response.status_code}")
    return file_path

# Transformation des données
def transform_data(file_paths):
    today = datetime.now().date()  # Valeur par défaut pour les dates manquantes
    disease_ids = {"covid_summary": 1, "h1n1": 2, "sars": 3, "monkeypox": 4}
    transformed_data = []

    for name, file_path in file_paths.items():
        print(f"Chargement des données de {name}...")
        df = pd.read_csv(file_path)
        print(f"En-têtes pour {name}: {list(df.columns)}")

        # Normalisation des colonnes
        if name == "covid_summary":
            df = df.rename(columns={
                "total_confirmed": "confirmed",
                "total_deaths": "deaths",
                "total_recovered": "recovered",
                "active_cases": "active",
                "total_tests": "total_tests"
            })
            df = df[["country", "confirmed", "deaths", "recovered", "active", "total_tests"]]
            df["_date"] = today

        elif name == "h1n1":
            df = df.rename(columns={
                "Date": "_date",
                "Country": "country",
                "Cumulative no. of cases": "confirmed",
                "Cumulative no. of deaths": "deaths"
            })
            df = df[["country", "_date", "confirmed", "deaths"]]
            df["_date"] = pd.to_datetime(df["_date"], errors="coerce").fillna(today)

        elif name == "sars":
            df = df.rename(columns={
                "Date": "_date",
                "Country": "country",
                "Cumulative number of case(s)": "confirmed",
                "Number of deaths": "deaths",
                "Number recovered": "recovered"
            })
            df = df[["country", "_date", "confirmed", "deaths", "recovered"]]
            df["_date"] = pd.to_datetime(df["_date"], errors="coerce").fillna(today)

        elif name == "monkeypox":
            df = df.rename(columns={
                "location": "country",
                "date": "_date",
                "total_cases": "confirmed",
                "total_deaths": "deaths"
            })
            df = df[["country", "_date", "confirmed", "deaths"]]
            df["_date"] = pd.to_datetime(df["_date"], errors="coerce").fillna(today)

        # Ajout de l'ID de maladie
        df["id_disease"] = disease_ids[name]
        transformed_data.append(df)

    return pd.concat(transformed_data, ignore_index=True)

# Vérification et ajout des maladies dans la table disease
def ensure_diseases_exist(conn, disease_ids):
    try:
        cursor = conn.cursor()
        # Vérifier les maladies existantes
        cursor.execute("SELECT id_disease FROM disease")
        existing_ids = {row[0] for row in cursor.fetchall()}
        missing_ids = set(disease_ids.values()) - existing_ids

        if missing_ids:
            print(f"Ajout des maladies manquantes : {missing_ids}")
            sql = "INSERT INTO disease (id_disease, name, is_pandemic) VALUES (%s, %s, %s)"
            values = [(int(id_), name, True) for name, id_ in disease_ids.items() if int(id_) in missing_ids]
            execute_batch(cursor, sql, values)
            conn.commit()
    except Exception as e:
        print(f"Erreur lors de l'ajout des maladies : {e}")

# Chargement des données dans PostgreSQL
def load_data_to_postgres(df):
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        print("Connexion à la base PostgreSQL réussie.")

        # Vérifier et ajouter les maladies manquantes
        disease_ids = {"covid_summary": 1, "h1n1": 2, "sars": 3, "monkeypox": 4}
        ensure_diseases_exist(conn, disease_ids)

        cursor = conn.cursor()

        # Insérer les données dans la table statement
        sql = """
        INSERT INTO statement (_date, confirmed, deaths, recovered, active, total_tests, id_disease)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        values = df[["_date", "confirmed", "deaths", "recovered", "active", "total_tests", "id_disease"]].values.tolist()
        execute_batch(cursor, sql, values)
        conn.commit()
        print("Données insérées avec succès dans la table statement.")
    except Exception as e:
        print(f"Erreur lors de l'insertion des données : {e}")
    finally:
        cursor.close()
        conn.close()

# Script principal
if __name__ == "__main__":
    file_paths = {name: download_file(name, url) for name, url in file_urls.items()}
    all_data = transform_data(file_paths)
    print(f"Données transformées :\n{all_data.head()}")
    load_data_to_postgres(all_data)
