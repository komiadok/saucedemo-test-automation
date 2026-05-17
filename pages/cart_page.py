# ===========================================
# ================= LIBRARY =================
# ===========================================

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# ===========================================
# ================== PAGE ===================
# ===========================================

class CartPage(BasePage):
    
    # ==============================
    # ========== LOCATORS ==========
    # ==============================
    
    ITEMS = (By.CLASS_NAME, "cart_item")
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    
    CHECKOUT_BTN = (By.ID, "checkout")
    
    
    # ==============================
    # ========== ACTIONS ===========
    # ==============================
    
    def continue_shopping(self):
        """Clique sur le bouton 'Continue Shopping'"""
        self.click((By.ID, "continue-shopping"))
    
    def remove_item_from_cart(self, name):
        """Retire un produit du panier"""
        for item in self.get_items():
            if item.find_element(*self.ITEM_NAME).text == name:
                item.find_element(By.CLASS_NAME, "cart_button").click()
                return
            
    def go_to_checkout(self):
        """Clique sur le bouton 'Checkout'"""
        self.click(self.CHECKOUT_BTN)
    
    # ==============================
    # ========== WAITERS ===========
    # ==============================
    
    def wait_checkout_btn(self):
        """Attend que le bouton 'Checkout' soit visible"""
        return self.wait_element_visible(self.CHECKOUT_BTN)
    
    def wait_continue_shopping_btn(self):
        """Attend que le bouton 'Continue Shopping' soit visible"""
        return self.wait_element_visible((By.ID, "continue-shopping"))
    
    def wait_inventory_page(self):
        """Attend que l'URL de la page contienne 'inventory'."""
        return self.wait_for_url_contains("inventory")
    
    def wait_item_disappeared(self, name):
        """Attend qu'un produit disparaisse de la page."""
        return self.wait_element_invisible((By.XPATH, f"//div[@class='inventory_item_name' and text()='{name}']"))
    
    def wait_checkout_page(self):
        """Attend que la page de checkout s'ouvre"""
        return self.wait_for_url_contains("checkout-step-one")
    
    # ==============================
    # ========== GETTERS ===========
    # ==============================
    
    def get_items(self):
        """Récupère les produits dans le panier."""
        return self.wait_all_elements_visible(self.ITEMS)
    
    def get_item_names(self):
        """Récupère le nom des produits."""
        return [
            item.find_element(*self.ITEM_NAME).text
            for item in self.get_items()
        ]
