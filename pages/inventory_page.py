# ===========================================
# ================= LIBRARY =================
# ===========================================

from selenium.webdriver.common.by import By
from pages.base_page import BasePage
from components.header_component import HeaderComponent

# ===========================================
# ================== PAGE ===================
# ===========================================

class InventoryPage(BasePage):
    
    # ==============================
    # ========== LOCATORS ==========
    # ==============================
    
    ITEMS = (By.CLASS_NAME, "inventory_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    
    SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    # ==============================
    # ======== CONSTRUCTEUR ========
    # ==============================
    
    def __init__(self, driver):
        super().__init__(driver)
        self.header = HeaderComponent(self)
        
    # ==============================
    # =========== ACTIONS ==========
    # ==============================
    
    def add_item_to_cart(self, name):
        """Ajoute un produit au panier."""
        for item in self.get_items():
            if item.find_element(*self.ITEM_NAME).text == name:
                item.find_element(By.CLASS_NAME, "btn_inventory").click()
                return
    
    def remove_item(self, name):
        """Supprime un produit du panier"""
        self.add_item_to_cart(name)
    
    # def go_to_cart(self):
    #     """Clique sur l'icône du panier pour accéder à la page du panier."""
    #     self.click(self.CART_ICON)
    
    def select_sort(self, option):
        """Sélectionne une option de tri"""
        self.select_dropdown_by_text(self.SORT_DROPDOWN, option)
    
    # ==============================
    # ========== GETTERS ===========
    # ==============================
    
    def get_items(self):
        """Récupère les produits affichés sur la page d'inventaire."""
        return self.wait_all_elements_visible(self.ITEMS)
    
    def get_items_data(self):
        """Extrait le nom et le prix des produits de la page d'inventaire."""
        return [
            {
                "name": item.find_element(*self.ITEM_NAME).text,
                "price": float(item.find_element(*self.ITEM_PRICE).text.replace("$", ""))
            }
            for item in self.get_items()
        ]
    
    def get_cart_count(self):
        """Retourne le nombre de produits dans le panier."""
        badge = self.wait_element_visible((By.CLASS_NAME, "shopping_cart_badge"))
        
        if not badge:
            return 0

        return int(badge.text)
    
    # ==============================
    # ========== WAITERS ===========
    # ==============================
    
    def wait_sort_dropdown(self):
        """Attend que le dropdown de tri s'affiche."""
        return self.wait_element_visible(self.SORT_DROPDOWN)
    
    def wait_item_elements_visible(self):
        """
        Attend que le nom, le prix et le bouton 'Add to cart' soient visibles pour chaque produit.
        """
        return [
            item.find_element(*self.ITEM_NAME).is_displayed() and
            item.find_element(*self.ITEM_PRICE).is_displayed() and
            item.find_element(By.CLASS_NAME, "btn_inventory").is_displayed()
            for item in self.get_items()
        ]
        
    def wait_cart_page(self):
        """Attend que l'URL de la page contienne 'cart'."""
        return self.wait_for_url_contains("cart")
    
    def wait_login_page(self):
        """Attend que la page de login s'affiche"""
        return self.wait_for_url("https://www.saucedemo.com/")
    
    # ==============================
    # ====== BUSINESS LOGIC ========
    # ==============================
    
    def sort_items(self, items, sort_option):
        """Retourne la liste triée attendue selon l'option sélectionnée."""

        if sort_option == "Name (A to Z)":
            return sorted(items, key=lambda x: x["name"])

        if sort_option == "Name (Z to A)":
            return sorted(items, key=lambda x: x["name"], reverse=True)

        if sort_option == "Price (low to high)":
            return sorted(items, key=lambda x: x["price"])

        if sort_option == "Price (high to low)":
            return sorted(items, key=lambda x: x["price"], reverse=True)

        raise ValueError(f"Option de tri inconnue : {sort_option}")