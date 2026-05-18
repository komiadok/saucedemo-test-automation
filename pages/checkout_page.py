# ===========================================
# ================= LIBRARY =================
# ===========================================

from selenium.webdriver.common.by import By
from pages.base_page import BasePage

# ===========================================
# ================== PAGE ===================
# ===========================================

class CheckoutPage(BasePage):
    
    # ==============================
    # ========== LOCATORS ==========
    # ==============================
    
    ERROR_MESSAGE =(By.CSS_SELECTOR, "h3[data-test='error']")
    
    CANCEL_BTN = (By.ID, "cancel")
    CONTINUE_BTN = (By.ID, "continue")
    
    # ==============================
    # ========== ACTIONS ===========
    # ==============================
    
    def cancel_checkout(self):
        """Annule le paiement."""
        self.click(self.CANCEL_BTN)
        
    def validate_checkout_form(self, firstname, lastname, zip):
        """Entre les informations de paiement et fait la validation."""
        self.type((By.ID, "first-name"), firstname)
        self.type((By.ID, "last-name"), lastname)
        self.type((By.ID, "postal-code"), zip)
        self.click(self.CONTINUE_BTN)
        
    def confirm_checkout(self):
        """Confirme le paiement."""
        self.click((By.ID, "finish"))
    
    # ==============================
    # ========== WAITERS ===========
    # ==============================
    
    def wait_form_elements(self):
        """Attend que tous les éléments du formulaire de paiement soient visible."""
        return self.wait_all_elements_visible((By.CLASS_NAME, "form_group"))
    
    def wait_continue_btn(self):
        """Attend que le bouton 'Continue' soit visible."""
        return self.wait_element_visible(self.CONTINUE_BTN)
    
    def wait_cancel_btn(self):
        """Attend que le bouton 'Cancel' soit visible."""
        return self.wait_element_visible(self.CANCEL_BTN)
    
    def wait_cart_page(self):
        """Attend que la page panier soit visible"""
        return self.wait_for_url_contains("cart")
    
    def wait_checkout_step_two(self):
        """Attend que l'étape 2 du paiement soit visible."""
        return self.wait_for_url_contains("checkout-step-two")
    
    def wait_back_home_btn(self):
        """Attend que le bouton 'Back Home' apparaisse."""
        return self.wait_element_visible((By.ID, "back-to-products"))
        
    # ==============================
    # ========== GETTERS ===========
    # ==============================
    
    def get_checkout_sucess_message(self):
        """Retourne le message de succès du paiement."""
        return self.get_text((By.CSS_SELECTOR, ".complete-header"))
    
    def get_item_price(self):
        """Récupère le prix du produit dans le récapitulatif de paiement."""
        price_text = self.get_text((By.CLASS_NAME, "summary_subtotal_label"))
        return self.extract_price(price_text)
    
    def get_tax(self):
        """Retourne la taxe affichée dans le récapitulatif de paiement."""
        tax_text = self.get_text((By.CLASS_NAME, "summary_tax_label"))
        return self.extract_price(tax_text)
    
    def get_total_price(self):
        """Retourne le prix total affiché dans le récapitulatif de paiement."""
        price_text = self.get_text((By.CLASS_NAME, "summary_total_label"))
        return self.extract_price(price_text)
    
    # ==============================
    # ====== BUSINESS LOGIC ========
    # ==============================
    
    def calculate_total_price(self):
        """Calcule le prix total d'un produit à partir de son prix de base et de la taxe."""
        return self.get_item_price() + self.get_tax()