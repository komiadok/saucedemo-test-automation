from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support import expected_conditions as EC

from config.settings import BASE_URL, DEFAULT_TIMEOUT

class BasePage:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, DEFAULT_TIMEOUT)

    def open(self, url=""):
        """Ouvre une page en utilisant l'URL de base et un chemin optionnel."""
        full_url = BASE_URL + url
        self.driver.get(full_url)

    def find_element_visible(self, locator):
        """Trouve un élément en utilisant un localisateur."""
        return self.wait.until(EC.visibility_of_element_located(locator))

    def find_elements_visible(self, locator):
        """Trouve plusieurs éléments en utilisant un localisateur."""
        return self.wait.until(EC.visibility_of_all_elements_located(locator))
    
    def find_element_clickable(self, locator):
        """Trouve un élément cliquable en utilisant un localisateur."""
        return self.wait.until(EC.element_to_be_clickable(locator))
    
    def wait_for_url(self, url):
        """Attend que l'URL actuelle corresponde à l'URL spécifiée."""
        return self.wait.until(EC.url_to_be(url))
    
    def wait_for_url_contains(self, text):
        """Attend que l'URL actuelle contienne un texte."""
        return self.wait.until(EC.url_contains(text))
    
    def click(self, locator):
        """Clique sur un élément trouvé par le localisateur."""
        self.find_element_clickable(locator).click()
        
    def input_text(self, locator, text):
        """Saisit du texte dans un champ trouvé par le localisateur."""
        element = self.find_element_visible(locator)
        element.clear()
        element.send_keys(text)
        
    def select_dropdown_by_visible_text(self, locator, text):
        """Sélectionne une option dans un dropdown par son texte visible."""
        select_element = self.find_element_visible(locator)
        select = Select(select_element)
        select.select_by_visible_text(text)
    
    def is_element_visible(self, locator):
        """Vérifie si un élément est visible sur la page."""
        try:
            self.find_element_visible(locator)
            return True
        except:
            return False
    
    def is_element_clickable(self, locator):
        """Vérifie si un élément est cliquable sur la page."""
        try:
            self.find_element_clickable(locator)
            return True
        except:
            return False
        
    def is_text_present(self, locator, text):
        """Vérifie si un texte spécifique est présent dans un élément trouvé par le localisateur."""
        try:
            element_text = self.get_text(locator)
            return text in element_text
        except:
            return False
    
    def get_current_url(self):
        """Récupère l'URL actuelle de la page."""
        return self.driver.current_url
    
    def get_attribute(self, locator, attribute):
        """Récupère la valeur d'un attribut d'un élément trouvé par le localisateur."""
        return self.find_element_visible(locator).get_attribute(attribute)
        
    def get_text(self, locator):
        """Récupère le texte d'un élément trouvé par le localisateur."""
        return self.find_element_visible(locator).text
    
    def get_elements_count(self, locator):
        """Récupère le nombre d'éléments trouvés par le localisateur."""
        return len(self.find_elements_visible(locator))
    
    def parse_price(self, price_text, currency_symbol="$"):
        """Parse un texte de prix et retourne sa valeur numérique."""
        
        if not price_text:
            raise ValueError("Prix vide ou introuvable")

        try:
            return float(price_text.replace(currency_symbol, "").strip())
        except ValueError:
            raise ValueError(f"Impossible de convertir le prix : {price_text}")
        
    def extract_data(self, elements, name_locator, price_locator, currency="$"):
        """Extrait les données d'une liste d'éléments d'inventaire, en récupérant le nom et le prix de chaque produit."""
        data = []
        for item in elements:
            name = item.find_element(*name_locator).text
            price_text = item.find_element(*price_locator).text
            price = self.parse_price(price_text, currency)

            data.append({
                "name": name,
                "price": price
            })
        return data
        