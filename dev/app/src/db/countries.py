import requests
import json
from psycopg2.extras import execute_batch  # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table
from db.pib import fetch_gdp_data

API_KEY = "UKRG6rVwuY8wXXfyE1ZWhg==Pu6zZccZayVbGrZi"
GDP_API_URL = "https://api.api-ninjas.com/v1/gdp?year=2020"
PAYS_REGION_JSON = "./json/pays_region.json"

CONTINENT_FIX = {
    "Americas": "South America",
    "Antarctic": "Antarctica"
}

def load_region_pays():
    try:
        with open(PAYS_REGION_JSON, "r", encoding="utf-8") as file:
            data = json.load(file)
        return {key.lower(): value for key, value in data.items()}
    except Exception as e:
        print(f"[ERROR] Impossible de charger {PAYS_REGION_JSON}: {e}")
        return {}

def fetch_climat_type():
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT id_climat_type, name FROM climat_type;")
        return {row[1].lower(): row[0] for row in cursor.fetchall()}
    except Exception as e:
        print(f"[ERROR] Problème lors de la récupération des ID climat: {e}")
        return {}
    finally:
        cursor.close()
        conn.close()

def set_data_countries():
    truncate_table("country")

    try:
        response = requests.get("https://restcountries.com/v3.1/all")
        response.raise_for_status()
        countries_data = response.json()
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème lors de la récupération des pays via l'API : {e}")
        return

    gdp_map = fetch_gdp_data(API_KEY, GDP_API_URL)
    region_pays = load_region_pays()
    climat_map = fetch_climat_type()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_continent, name FROM continent;")
        continent_map = {row[1]: row[0] for row in cursor.fetchall()}

        values = []
        for country in countries_data:
            name = country.get("name", {}).get("common", "").strip()
            population = country.get("population")
            region = country.get("region", "").strip()
            iso_code = country.get("cca3", "").strip()

            if not name or not population or not region or not iso_code:
                continue

            region = CONTINENT_FIX.get(region, region)
            id_continent = continent_map.get(region)

            if not id_continent:
                print(f"[WARNING] Continent inconnu pour {name} (Région: {region})")
                continue

            pib = gdp_map.get(iso_code, None)

            region_data = region_pays.get(name.lower())  
            id_climat_type = region_data.get("code_climat") if region_data else None

            if id_climat_type not in climat_map.values():
                print(f"[WARNING] ID climat {id_climat_type} non trouvé en base pour {name}, assignation de NULL")
                id_climat_type = None 

            if not pib or not id_climat_type :
                continue

            values.append((name, population, id_continent, pib, id_climat_type))

        if not values:
            print("[ERROR] Aucun pays valide à insérer.")
            return

        sql = """
            INSERT INTO country (name, population, id_continent, pib, id_climat_type)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (name) DO NOTHING;
        """
        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(values)} pays insérés dans la table 'country'.")

    except Exception as e:
        print(f"[ERROR] Problème lors de l'insertion des pays en base : {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
