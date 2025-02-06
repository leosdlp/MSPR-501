from psycopg2.extras import execute_batch  # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


def set_disease(disease):
    conn = get_connection()
    cursor = conn.cursor()

    truncate_table("disease")

    sql = "INSERT INTO disease (id_disease, name, is_pandemic) VALUES (%s, %s, %s)"

    values = [
        (data["id"], name, data["isPandemic"]) 
        for name, data in disease.items()
    ]

    execute_batch(cursor, sql, values)
    conn.commit()
    cursor.close()
    conn.close()
