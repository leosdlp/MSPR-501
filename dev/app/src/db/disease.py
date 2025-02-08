"""
Ce module permet de gérer les maladies dans la base de données, y compris l'insertion des données dans la 
table `disease`. Il inclut une fonction pour insérer les informations des maladies à partir d'un 
dictionnaire dans la base de données après avoir vidé la table.
"""

from psycopg2.extras import execute_batch  # type: ignore

from db.connection import get_connection
from db.truncate_table import truncate_table


def set_disease(disease):
    """
    Insère les données des maladies dans la table `disease`.

    Cette fonction prend un dictionnaire de maladies, où chaque clé est le nom de la maladie et chaque 
    valeur est un dictionnaire contenant l'ID de la maladie et un indicateur si la maladie est pandémique. 
    Elle vide d'abord la table `disease` avec la fonction `truncate_table`, puis insère les données dans 
    la base de données via une requête SQL préparée.
    
    La fonction utilise `execute_batch` pour insérer les données en lot, ce qui améliore les performances 
    d'insertion pour un grand nombre de données.

    Args:
        disease (dict): Dictionnaire des maladies, où la clé est le nom de la maladie et la valeur est un 
        dictionnaire avec `id` et `isPandemic`.

    Returns:
        None
    """
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

    print("[INFO] Données insérées dans la table disease.")

    cursor.close()
    conn.close()
