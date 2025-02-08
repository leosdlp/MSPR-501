from psycopg2.extras import execute_batch # type: ignore
import json

from db.connection import get_connection
from db.truncate_table import truncate_table


CLIMAT_TYPE_JSON = "./json/climat_type.json"

def set_climat_type():
    """ Insère les types de climat dans la base de données """
    try:
        with open(CLIMAT_TYPE_JSON, "r", encoding="utf-8") as file:
            climat_types = json.load(file)
        print(f"[INFO] Chargement de {len(climat_types)} types de climat depuis {CLIMAT_TYPE_JSON}.")
    except Exception as e:
        print(f"[ERROR] Impossible de charger {CLIMAT_TYPE_JSON}: {e}")
        return

    conn = get_connection()
    cursor = conn.cursor()

    try:
        truncate_table("climat_type")  # Nettoie la table avant insertion

        sql = """
            INSERT INTO climat_type (id_climat_type, name, description)
            VALUES (%s, %s, %s);
        """

        values = [(i + 1, climat["name"], climat["description"]) for i, climat in enumerate(climat_types)]

        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(values)} types de climat insérés dans la table 'climat_type'.")

    except Exception as e:
        print(f"[ERROR] Problème lors de l'insertion des types de climat en base : {e}")
        conn.rollback()

    finally:
        cursor.close()
        conn.close()
