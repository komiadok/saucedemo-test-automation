from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from core.logger import logger

class LoginPage(BasePage):
    # Locators pour les éléments de la page de connexion
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BUTTON = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    def open_login_page(self):
        """Ouvre la page de connexion."""
        logger.info("🌐 Ouverture de la page de connexion")
        self.open()
    
    def login(self, username, password):
        """Effectue une tentative de connexion avec les informations d'identification fournies."""
        logger.info("📝 Saisie des identifiants de connexion")
        self.input_text(self.USERNAME_INPUT, username)
        self.input_text(self.PASSWORD_INPUT, password)
        logger.info("🔐 Tentative de connexion")
        self.click(self.LOGIN_BUTTON)
        
    def is_login_successful(self):
        """Vérifie si la connexion a réussi en vérifiant que l'URL contient '/inventory'."""
        logger.info("🔍 Vérification de la réussite de la connexion")
        return self.wait_for_url_contains("/inventory")

    def is_error_message_displayed(self):
        """Vérifie si le message d'erreur est affiché après une tentative de connexion échouée."""
        logger.info("🔍 Vérification de l'affichage du message d'erreur")
        return self.is_element_visible(self.ERROR_MESSAGE)
    
    def get_error_message(self):
        """Retourne le message d'erreur affiché après un login invalide."""
        return self.get_text(self.ERROR_MESSAGE)
    
    def is_error_message_valid(self, expected_message):
        """Vérifie que le message d'erreur affiché correspond au message attendu."""
        return self.is_text_present(self.ERROR_MESSAGE, expected_message)
    