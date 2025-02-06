from db.countries import set_data_countries
from db.continents import set_data_continents


def set_data_immutable():
    print(" ========== Insertion des données dans continent ========== ")
    set_data_continents()

    print(" ========== Insertion des données dans country ========== ")
    set_data_countries()
