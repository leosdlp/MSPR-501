import os
import shutil


def drop_dataset():
    data_folder = "./data_files"
    
    try:
        if not os.path.exists(data_folder):
            raise FileNotFoundError(f"Le dossier '{data_folder}' n'existe pas.")
        else:
            shutil.rmtree(data_folder)
            print(f"[INFO] Dossier supprimé : {data_folder}")
    except Exception as e:
        print(f"[ERROR] {e}")
