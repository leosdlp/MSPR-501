from db.countries import set_data_countries
from db.continents import set_data_continents
from db.climat_type import set_climat_type
from db.region import set_region


def set_data_immutable():
    print("\n ===== Insertion des données dans climat_type ===== ")
    set_climat_type()

    print("\n ===== Insertion des données dans continent ===== ")
    set_data_continents()

    print("\n ===== Insertion des données dans region ===== ")
    set_region()

    print("\n ===== Insertion des données dans country ===== ")
    set_data_countries()