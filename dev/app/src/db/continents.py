from psycopg2.extras import execute_batch  # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


def set_data_continents():
    truncate_table("continent")

    continents = [
        "Africa", "Antarctica", "Asia", "Europe", "North America", "Oceania", "South America"
    ]

    conn = get_connection()
    cursor = conn.cursor()

    try:
        sql = "INSERT INTO continent (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;"
        values = [(continent,) for continent in continents]

        execute_batch(cursor, sql, values)
        conn.commit()
        print(f"[INFO] {len(continents)} continents insérés dans la table 'continent'.")
    
    except Exception as e:
        print(f"[ERROR] Problème lors de l'insertion des continents : {e}")
        conn.rollback()
    
    finally:
        cursor.close()
        conn.close()
