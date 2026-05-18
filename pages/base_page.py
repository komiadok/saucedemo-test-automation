# ===========================================
# ================= LIBRARY =================
# ===========================================

from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC
from config.settings import BASE_URL, DEFAULT_TIMEOUT

# ===========================================
# ================== PAGE ===================
# ===========================================

class BasePage:
    
    # ==============================
    # ======== CONSTRUCTEUR ========
    # ==============================
    
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    # ==============================
    # =========== ACTIONS ==========
    # ==============================
    
    def open(self, path=""):
        """Ouvre une page en utilisant l'URL de base et un chemin (optionnel)."""
        self.driver.get(BASE_URL + path)

    
    def click(self, locator):
        """Clique sur un élément trouvé par le localisateur."""
        self.wait_element_clickable(locator).click()
        
    def select_dropdown_by_text(self, locator, text):
        """Sélectionne une option dans un dropdown par son texte visible."""
        Select(self.wait_element_visible(locator)).select_by_visible_text(text)
    
    def type(self, locator, text):
        """Saisit du texte dans un champ trouvé par le localisateur."""
        el = self.wait_element_visible(locator)
        el.clear()
        el.send_keys(text)
    
    # ==============================
    # ========== WAITERS ===========
    # ==============================
    
    def wait_element_visible(self, locator):
        """Attend que l'élément du locator soit visible sur la page."""
        return self.wait.until(EC.visibility_of_element_located(locator))
    
    def wait_all_elements_visible(self, locator):
        """Attend que tous les éléments du locator soit visibles sur la page."""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))
    
    def wait_element_invisible(self, locator):
        return self.wait.until(EC.invisibility_of_element_located(locator))
    
    def wait_element_clickable(self, locator):
        """Attend que l'élément du locator soit cliquable."""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_url(self, url):
        """Attend que l'URL actuelle corresponde à l'URL spécifiée."""
        return self.wait.until(EC.url_to_be(url))
    
    def wait_for_url_contains(self, text):
        """Attend que l'URL actuelle contienne un texte."""
        return self.wait.until(EC.url_contains(text))
    
    # ==============================
    # ========== GETTERS ===========
    # ==============================
    
    def get_text(self, locator):
        """Récupère le texte d'un élément trouvé par le localisateur."""
        return self.wait_element_visible(locator).text
    
    # ==============================
    # ====== BUSINESS LOGIC ========
    # ==============================
    
    def extract_price(self, price_text):
        """Extrait un prix depuis un texte."""
        return float(
            price_text
            .split("$")[1]
            .strip()
        )
    

    
        