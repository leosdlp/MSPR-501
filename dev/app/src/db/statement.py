from psycopg2.extras import execute_batch  # type: ignore

from db.connection import get_connection

def set_statement_data(df):
    if df.empty:
        raise Exception("[ERROR] Empty DataFrame")
    
    conn = get_connection()
    cursor = conn.cursor()

    sql = """
        INSERT INTO statement (_date, confirmed, deaths, recovered, active, total_tests, id_disease)
        VALUES (%s, %s, %s, %s, %s, %s, %s);
    """

    values = df[["_date", "confirmed", "deaths", "recovered", "active", "total_tests", "id_disease"]].values.tolist()
    
    execute_batch(cursor, sql, values)

    conn.commit()
    cursor.close()
    conn.close()

