# ===========================================
# ================= LIBRARY =================
# ===========================================

from selenium.webdriver.common.by import By

# ===========================================
# ================= HEADER ==================
# ===========================================

class HeaderComponent:

    # ==============================
    # ========== LOCATORS ==========
    # ==============================
    
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    MENU_BTN = (By.ID, "react-burger-menu-btn")
    LOGOUT_BTN = (By.ID, "logout_sidebar_link")
    
    # ==============================
    # ======== CONSTRUCTEUR ========
    # ==============================
    
    def __init__(self, page):
        self.page = page

    # ==============================
    # ========== ACTIONS ===========
    # ==============================
    
    def open_cart(self):
        """Ouvre le panier."""
        self.page.click(self.CART_ICON)

    def open_menu(self):
        """Ouvre le menu latéral."""
        self.page.click(self.MENU_BTN)

    def logout(self):
        """Réalise la déconnexion"""
        self.page.click(self.LOGOUT_BTN)
        
    # ==============================
    # ========== WAITERS ===========
    # ==============================
    
    def wait_cart_icon(self):
        """Attend que l'icône du panier s'affiche."""
        return self.page.wait_element_visible(self.CART_ICON)
    
    def wait_menu_btn(self):
        return self.page.wait_element_visible(self.MENU_BTN)