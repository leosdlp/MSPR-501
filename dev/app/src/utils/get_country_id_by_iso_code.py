from utils.get_country_code_by_name import get_country_code_by_name as get_country_code

def get_country_id(country_name, countries):
        """Retourne l'id du pays si le code ISO2 est en base, sinon None"""
        iso_code = get_country_code(country_name)  # Conversion du nom en code ISO2
        return countries.get(iso_code, None)