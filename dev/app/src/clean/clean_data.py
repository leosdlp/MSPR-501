from dev.app.src.db.statement import set_statement_data
from clean.clean_covid import clean_covid
from clean.clean_h1n1 import clean_h1n1
from clean.clean_mpox import clean_mpox
from clean.clean_sras import clean_sras

def clean_data():
    print(" ========== Nettoyage des données pour covid ========== ")
    df = clean_covid()
    try:
        df = set_statement_data(df)
    except Exception as e:
        print(e)

    print(" ========== Nettoyage des données pour h1n1 ========== ")
    df = clean_h1n1()
    try:
        df = set_statement_data(df)
    except Exception as e:
        print(e)  

    print(" ========== Nettoyage des données pour mpox ========== ")
    df = clean_mpox()
    try:
        df = set_statement_data(df)
    except Exception as e:
        print(e)

    print(" ========== Nettoyage des données pour sras ========== ")
    df = clean_sras()
    try:
        df = set_statement_data(df)
    except Exception as e:
        print(e)
