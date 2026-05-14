import os
import json
from datetime import datetime
import allure

def get_current_timestamp() -> str:
    """Retourne un timestamp formaté pour les fichiers."""
    return datetime.now().strftime("%Y-%m-%d_%H-%M-%S")


def read_json(file_path: str) -> dict:
    """Lit un fichier JSON et retourne son contenu."""
    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)

SCREENSHOT_DIR = "reports/screenshots"

def take_screenshot(driver, test_name):
    """    
    Prend un screenshot, le sauvegarde et l'attache à Allure.
    
    Retourne le chemin du fichier.
    """
    
    # Création du dossier de screenshots s'il n'existe pas
    os.makedirs(SCREENSHOT_DIR, exist_ok=True)
    
    # Génération du nom de fichier
    timestamp = get_current_timestamp()
    file_name = f"{test_name}_{timestamp}.png"
    path = os.path.join(SCREENSHOT_DIR, file_name)
    
    # Capture écran via Selenium
    driver.save_screenshot(path)
    
    # Attache au rapport Allure
    allure.attach.file(
        path,
        name=file_name,
        attachment_type=allure.attachment_type.PNG
    )

    return path