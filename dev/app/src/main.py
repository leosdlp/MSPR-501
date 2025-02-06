import time

from data.get_brut_data import get_brut_data
from db.disease import set_disease
from db.data_immutable import set_data_immutable
from clean.clean_data import clean_data


DISEASE = {
            "covid_summary": { "id": 1, "isPandemic": True },
            "h1n1": { "id": 2,"isPandemic": True },
            "sars": { "id": 3,"isPandemic": False },
            "monkeypox": { "id": 4,"isPandemic": False }
            }

time.sleep(10) # ATENTION : À SUPPRIMER (délais le temps que les containers nécessaires au traitement se montent)

print(" ========== Début de la récupération des datas brutes ========== ")
get_brut_data()

print(" ========== Insertion des données dans disease ========== ")
set_disease(DISEASE)

print(" ========== Insertion des données fixes dans les tables ========== ")
set_data_immutable()

print(" ========== Nettoyage et insertion des données dans statement ========== ")
clean_data()