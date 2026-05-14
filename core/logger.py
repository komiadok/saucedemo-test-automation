import logging
import os
from core.utils import get_current_timestamp

# --- Dossier de logs ---
LOG_DIR = "logs"
os.makedirs(LOG_DIR, exist_ok=True)

# --- Nom du fichier de log avec timestamp ---
timestamp = get_current_timestamp()
log_file = os.path.join(LOG_DIR, f"execution_{timestamp}.log")

# --- Création du logger ---
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Évite d'ajouter plusieurs handlers si le module est rechargé
if not logger.handlers:

    # Handler fichier
    file_handler = logging.FileHandler(log_file, encoding="utf-8")
    file_handler.setLevel(logging.INFO)

    # Format des logs
    formatter = logging.Formatter(
        "%(asctime)s | %(name)s | %(levelname)s | %(message)s"
    )
    file_handler.setFormatter(formatter)

    logger.addHandler(file_handler)