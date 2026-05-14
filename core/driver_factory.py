from selenium import webdriver
from config.settings import HEADLESS, BROWSER

def create_driver():

    if BROWSER == "chrome":
        options = webdriver.ChromeOptions()

        if HEADLESS:
            options.add_argument("--headless=new")

        options.add_argument("--start-maximized")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-popup-blocking")

        prefs = {
            "profile.password_manager_leak_detection": False,
            "credentials_enable_service": False,
            "profile.password_manager_enabled": False
        }

        options.add_experimental_option("prefs", prefs)

        driver = webdriver.Chrome(options=options)

    return driver