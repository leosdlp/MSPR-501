from db.connection import get_connection


def truncate_table(table):
    conn = get_connection()
    cursor = conn.cursor()

    sql = f"TRUNCATE TABLE {table} RESTART IDENTITY CASCADE;"

    cursor.execute(sql)
    conn.commit()

    print(f"[INFO] Table {table} vidée.")

    cursor.close()
    conn.close()
