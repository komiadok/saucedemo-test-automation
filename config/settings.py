import os
from dotenv import load_dotenv

# Charger le fichier .env
load_dotenv()

# =========================
# Application URL
# =========================
BASE_URL = os.getenv("BASE_URL", "https://www.saucedemo.com/")

# =========================
# Browser config
# =========================
BROWSER = os.getenv("BROWSER", "chrome").lower()

HEADLESS = os.getenv("HEADLESS", "false").lower() == "true"

# =========================
# Timeouts
# =========================
DEFAULT_TIMEOUT = int(os.getenv("DEFAULT_TIMEOUT", 10))