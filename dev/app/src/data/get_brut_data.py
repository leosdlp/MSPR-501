import os
import requests
import zipfile
import io
from pyspark.sql import SparkSession  # type: ignore

spark = SparkSession.builder.appName("ReadCSVFromZip").getOrCreate()

urls = [
    "https://www.kaggle.com/api/v1/datasets/download/imdevskp/h1n1-swine-flu-2009-pandemic-dataset",
    "https://www.kaggle.com/api/v1/datasets/download/imdevskp/corona-virus-report",
    "https://www.kaggle.com/api/v1/datasets/download/josephassaker/covid19-global-dataset",
    "https://www.kaggle.com/api/v1/datasets/download/utkarshx27/mpox-monkeypox-data",
    "https://www.kaggle.com/api/v1/datasets/download/imdevskp/sars-outbreak-2003-complete-dataset"
]

def get_brut_data():
    data_folder = "./data_files"

    if not os.path.exists(data_folder):
        os.makedirs(data_folder)
        print(f"Dossier créé : {data_folder}")

    for url in urls:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            print(f"Archive téléchargée avec succès depuis : {url}")
            
            zip_name = url.split("/")[-1].split("?")[0]
            zip_folder = os.path.join(data_folder, zip_name)
            if not os.path.exists(zip_folder):
                os.makedirs(zip_folder)
                print(f"Dossier créé pour l'archive : {zip_folder}")
            
            with zipfile.ZipFile(io.BytesIO(response.content)) as z:
                print("Fichiers contenus dans l'archive :")
                print(z.namelist())
                
                for file_name in z.namelist():
                    if file_name.endswith(".csv"):
                        print(f"\nExtraction et lecture du fichier : {file_name}")
                        file_path = os.path.join(zip_folder, file_name)
                        
                        with z.open(file_name) as f:
                            with open(file_path, "wb") as extracted_file:
                                extracted_file.write(f.read())
                        
                        df = spark.read.csv(file_path, header=True, inferSchema=True)
                        df.show(5)
        else:
            print(f"Échec du téléchargement depuis {url}. Code d'état : {response.status_code}")
