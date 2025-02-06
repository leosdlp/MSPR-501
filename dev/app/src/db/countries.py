import requests
from psycopg2.extras import execute_batch  # type: ignore
from db.connection import get_connection
from db.truncate_table import truncate_table

API_KEY = "UKRG6rVwuY8wXXfyE1ZWhg==Pu6zZccZayVbGrZi"
GDP_API_URL = "https://api.api-ninjas.com/v1/gdp?year=2020"

CONTINENT_FIX = {
    "Americas": "South America",
    "Antarctic": "Antarctica"
}

def fetch_gdp_data():
    """ Récupère les données de PIB nominal (en milliards USD) pour l'année 2020 depuis l'API API-Ninjas. """
    try:
        print(f"[INFO] Récupération des données de PIB depuis {GDP_API_URL}")
        response = requests.get(GDP_API_URL, headers={'X-Api-Key': API_KEY})
        response.raise_for_status()
        data = response.json()

        if not data:
            print("[WARNING] Aucune donnée valide récupérée pour le PIB.")
            return {}

        print(f"[INFO] {len(data)} enregistrements de PIB récupérés.")

        gdp_map = {}
        for entry in data:
            country_code = entry.get("country") 
            gdp_nominal = entry.get("gdp_nominal") 

            if country_code and gdp_nominal is not None:
                gdp_map[country_code] = gdp_nominal * 1_000_000_000

        return gdp_map

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème lors de la récupération des données du PIB : {e}")
        return {}

def set_data_countries():
    truncate_table("country")

    url = "https://restcountries.com/v3.1/all"

    try:
        print(f"[INFO] Récupération des données des pays depuis {url}")
        response = requests.get(url)
        response.raise_for_status()
        countries_data = response.json()

        if not countries_data:
            print("[ERROR] Aucune donnée de pays récupérée.")
            return

        print(f"[INFO] {len(countries_data)} pays récupérés.")

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème lors de la récupération des pays via l'API : {e}")
        return

    gdp_map = fetch_gdp_data()

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT id_continent, name FROM continent;")
        continent_map = {row[1]: row[0] for row in cursor.fetchall()}
        print("[INFO] Mapping des continents récupéré.")

        values = []
        for country in countries_data:
            name = country.get("name", {}).get("common")
            population = country.get("population")
            region = country.get("region")
            iso_code = country.get("cca3")

            if not name or not population or not region or not iso_code:
                continue

            # Correction du continent si nécessaire
            region = CONTINENT_FIX.get(region, region)
            id_continent = continent_map.get(region)

            if not id_continent:
                print(f"[WARNING] Continent inconnu pour le pays : {name} (Région: {region})")
                continue

            pib = gdp_map.get(iso_code) 

            if pib is None:
                pib = -1


            values.append((name, population, id_continent, pib))

        if not values:
            print("[ERROR] Aucun pays valide à insérer.")
            return

        sql = """
            INSERT INTO country (name, population, id_continent, pib)
            VALUES (%s, %s, %s, %s)
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
