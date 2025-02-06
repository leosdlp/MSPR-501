import requests


def fetch_gdp_data(API_KEY, GDP_API_URL):
    """ Récupère les données de PIB nominal (en milliards USD) pour l'année 2020 depuis l'API API-Ninjas. """
    try:
        print(f"[INFO] Récupération des données de PIB depuis {GDP_API_URL}")
        response = requests.get(GDP_API_URL, headers={'X-Api-Key': API_KEY})
        response.raise_for_status()
        data = response.json()

        if not data:
            print("[WARNING] Aucune donnée valide récupérée pour le PIB.")
            return {}

        print(f"[INFO] {len(data)} enregistrements de PIB récupérés.")

        gdp_map = {}
        for entry in data:
            country_code = entry.get("country")
            gdp_nominal = entry.get("gdp_nominal")

            if country_code and gdp_nominal is not None:
                gdp_map[country_code] = gdp_nominal * 1_000_000_000  # Conversion en dollars

        return gdp_map

    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Problème lors de la récupération des données du PIB : {e}")
        return {}