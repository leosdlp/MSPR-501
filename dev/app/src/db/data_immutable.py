from db.countries import set_data_countries
from db.continents import set_data_continents
from db.climat_type import set_climat_type


def set_data_immutable():
    print(" ========== Insertion des données dans climat_type ========== ")
    set_climat_type()

    print(" ========== Insertion des données dans continent ========== ")
    set_data_continents()

    print(" ========== Insertion des données dans country ========== ")
    set_data_countries()
