# ===========================================
# ================= LIBRARY =================
# ===========================================

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# ===========================================
# ================== PAGE ===================
# ===========================================

class LoginPage(BasePage):
    
    # ==============================
    # ========== LOCATORS ==========
    # ==============================
    
    USERNAME_INPUT = (By.ID, "user-name")
    PASSWORD_INPUT = (By.ID, "password")
    LOGIN_BTN = (By.ID, "login-button")
    ERROR_MESSAGE = (By.CSS_SELECTOR, "[data-test='error']")
    
    # ==============================
    # ========== ACTIONS ==========
    # ==============================
    
    def open_login_page(self):
        """Ouvre la page de connexion avec le chemin fourni (optionnel)."""
        self.open()
    
    def login(self, username, password):
        """Effectue une tentative de connexion avec les informations d'identification fournies."""
        self.type(self.USERNAME_INPUT, username)
        self.type(self.PASSWORD_INPUT, password)
        self.click(self.LOGIN_BTN)
    
    # ==============================
    # ========== GETTERS ===========
    # ==============================
        
    def get_error_message(self):
        """Retourne le message d'erreur affiché après un login invalide."""
        return self.get_text(self.ERROR_MESSAGE)
    
    # ==============================
    # ========== WAITERS ==========
    # ==============================
        
    def wait_inventory_page(self):
        """Attend que l'URL de la page contienne 'inventory'."""
        return self.wait_for_url_contains("inventory")
    