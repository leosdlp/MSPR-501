from psycopg2.extras import execute_batch  # type: ignore
import json

from db.connection import get_connection
from db.truncate_table import truncate_table


PAYS_REGION_JSON = "./json/pays_region.json"

def get_existing_countries():
    """Récupère les pays existants en base avec leur ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_country, name FROM country;")
    countries = {name.lower(): id for id, name in cursor.fetchall()}
    cursor.close()
    conn.close()
    return countries

def get_existing_climat_types():
    """Récupère les types de climat existants en base avec leur ID"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT id_climat_type, name FROM climat_type;")
    climat_types = {name.lower(): id for id, name in cursor.fetchall()}
    cursor.close()
    conn.close()
    return climat_types

def insert_country_climat_types():
    """Insère les relations pays-climat dans la table pivot"""
    with open(PAYS_REGION_JSON, "r", encoding="utf-8") as file:
        pays_data = json.load(file)

    country_map = get_existing_countries()
    climat_map = get_existing_climat_types()

    conn = get_connection()
    cursor = conn.cursor()

    truncate_table("country_climat_type")

    values = []
    for country_name, data in pays_data.items():
        country_id = country_map.get(country_name.lower())

        if not country_id:
            continue
        
        for climat in data["climat"]:
            climat_id = climat_map.get(climat.lower())
            if not climat_id:
                print(f"[WARNING] Climat '{climat}' non trouvé en base, ignoré.")
                continue
            values.append((country_id, climat_id))
            print(f"[INFO] Préparation de la relation pays-climat : {country_name} - {climat}")
    
    if not values:
        print("[ERROR] Aucun pays-climat valide à insérer.")
        return

    sql = """
        INSERT INTO country_climat_type (id_country, id_climat_type)
        VALUES (%s, %s);
    """
    try:
        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(values)} relations pays-climat insérées dans 'country_climat_type'.")
    except Exception as e:
        conn.rollback()
        print(f"[ERROR] Problème lors de l'insertion des pays-climats : {e}")
    finally:
        cursor.close()
        conn.close()

