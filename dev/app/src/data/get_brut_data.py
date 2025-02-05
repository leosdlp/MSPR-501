import os
import requests

file_urls = {
    "covid_daily": "https://lab.enzo-palermo.com/mspr501/data/mondial-covid-19/worldometer_coronavirus_daily_data.csv",
    "h1n1": "https://lab.enzo-palermo.com/mspr501/data/h1n1/data.csv",
    "sars": "https://lab.enzo-palermo.com/mspr501/data/sars_2003/sars_2003_complete_dataset_clean.csv",
    "monkeypox": "https://lab.enzo-palermo.com/mspr501/data/variole-du-singe/owid-monkeypox-data.csv"
}

def download_file(name, url, download_dir="data_files"):
    os.makedirs(download_dir, exist_ok=True)
    file_path = os.path.join(download_dir, f"{name}.csv")
    if not os.path.exists(file_path):
        print(f"Téléchargement de {name} depuis {url}...")
        response = requests.get(url)
        if response.status_code == 200:
            with open(file_path, "wb") as f:
                f.write(response.content)
            print(f"Fichier {name} téléchargé avec succès.")
        else:
            raise Exception(f"Erreur lors du téléchargement de {name}: {response.status_code}")
    return file_path

def get_brut_data():
    for name, file_url in file_urls.items():
        download_file(name, file_url)