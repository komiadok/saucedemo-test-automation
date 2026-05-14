import logging
import os
from datetime import datetime


def get_logger(test_name: str) -> logging.Logger:

    # =========================
    # Créer le dossier logs
    # =========================
    os.makedirs("logs", exist_ok=True)

    # =========================
    # Date/heure
    # =========================
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

    # =========================
    # Nom du fichier log
    # =========================
    log_file = f"logs/{test_name}_{timestamp}.log"

    # =========================
    # Logger
    # =========================
    logger = logging.getLogger(test_name)

    # Évite les doublons
    if logger.hasHandlers():
        return logger

    logger.setLevel(logging.INFO)

    # =========================
    # Format
    # =========================
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    # =========================
    # Console
    # =========================
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    # =========================
    # Fichier
    # =========================
    file_handler = logging.FileHandler(
        log_file,
        encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    # =========================
    # Ajouter handlers
    # =========================
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    return logger