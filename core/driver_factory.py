from selenium import webdriver
from config.settings import HEADLESS, BROWSER

def create_driver():
    """Crée une instance de WebDriver."""
    
    if BROWSER != "chrome":
        raise ValueError(f"Browser non supporté : {BROWSER}")
    
    options = webdriver.ChromeOptions()

    if HEADLESS:
        options.add_argument("--headless=new")
    
    options.add_argument("--window-size=1920,1080")
    options.add_argument("--disable-notifications")
    options.add_argument("--disable-popup-blocking")

    prefs = {
        "profile.password_manager_leak_detection": False,
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    }

    options.add_experimental_option("prefs", prefs)

    return webdriver.Chrome(options=options)