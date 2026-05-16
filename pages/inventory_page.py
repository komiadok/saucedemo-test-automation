from pages.base_page import BasePage
from selenium.webdriver.common.by import By

from config.settings import BASE_URL

from core.logger import logger

class InventoryPage(BasePage):
    # Locators pour les éléments de la page d'inventaire
    PAGE_TITLE = (By.CLASS_NAME, "title")
    INVENTORY_ITEMS = (By.CLASS_NAME, "inventory_item")
    
    ITEM_NAME = (By.CLASS_NAME, "inventory_item_name")
    ITEM_PRICE = (By.CLASS_NAME, "inventory_item_price")
    
    CART_ICON = (By.CLASS_NAME, "shopping_cart_link")
    CART_BADGE = (By.CLASS_NAME, "shopping_cart_badge")
    
    ADD_TO_CART_BUTTON = (By.CLASS_NAME, "btn_inventory")
    
    ITEM_SORT_DROPDOWN = (By.CLASS_NAME, "product_sort_container")
    
    BURGER_MENU_BUTTON = (By.ID, "react-burger-menu-btn")
    LOGOUT_LINK = (By.ID, "logout_sidebar_link")
    
    def is_page_title_displayed(self):
        """Vérifie si le titre de la page d'inventaire est affiché."""
        return self.is_element_visible(self.PAGE_TITLE)
    
    def get_page_title(self):
        """Récupère le texte du titre de la page d'inventaire."""
        return self.get_text(self.PAGE_TITLE)
    
    def is_page_title_correct(self, expected_title):
        """Vérifie si le titre de la page d'inventaire correspond au titre attendu."""
        return self.is_text_present(self.PAGE_TITLE, expected_title)
    
    def is_cart_icon_displayed(self):
        """Vérifie si l'icône du panier est affichée sur la page d'inventaire."""
        return self.is_element_visible(self.CART_ICON)
    
    def is_burger_menu_displayed(self):
        """Vérifie si le bouton du menu burger est affiché sur la page d'inventaire."""
        return self.is_element_visible(self.BURGER_MENU_BUTTON)
    
    def is_sort_dropdown_displayed(self):
        """Vérifie si le dropdown de tri est affiché sur la page d'inventaire."""
        return self.is_element_visible(self.ITEM_SORT_DROPDOWN)
    
    def is_inventory_items_displayed(self):
        """Vérifie si les articles sont affichés sur la page d'inventaire."""
        return self.is_element_visible(self.INVENTORY_ITEMS)
    
    def get_inventory_items_count(self):
        """Récupère le nombre d'articles affichés sur la page d'inventaire."""
        return self.get_elements_count(self.INVENTORY_ITEMS)
    
    def is_inventory_item_valid(self, item):
        """
        Vérifie qu'un item contient :
        - un nom de produit
        - un prix
        - un bouton Add to cart
        """
        try:
            item.find_element(*self.ITEM_NAME).is_displayed()
            item.find_element(*self.ITEM_PRICE).is_displayed()
            item.find_element(*self.ADD_TO_CART_BUTTON).is_displayed()
            return True

        except Exception:
            return False
    
    def are_all_inventory_items_valid(self):
        """Vérifie que tous les items de l'inventaire sont valides."""
        items = self.find_elements_visible(self.INVENTORY_ITEMS)
        
        return all(
            self.is_inventory_item_valid(item)
            for item in items
        )
    
    def extract_items_order(self):
        """Extrait l'ordre d'apparition des produits sur la page."""
        items = self.find_elements_visible(self.INVENTORY_ITEMS)
        return self.extract_data(items, self.ITEM_NAME, self.ITEM_PRICE)
    
    def select_sort_option(self, option_text):
        """Sélectionne une option dans le dropdown de tri."""
        self.select_dropdown_by_visible_text(self.ITEM_SORT_DROPDOWN, option_text)
        
    def get_expected_sorted_items_order(self, before_sort_data, sort_option): 
        """Retourne l'ordre d'apparition attendu des produits après tri en fonction de l'option de tri sélectionnée."""
        
        if sort_option == "Name (A to Z)":
            return sorted(before_sort_data, key=lambda x: x["name"])
        elif sort_option == "Name (Z to A)":
            return sorted(before_sort_data, key=lambda x: x["name"], reverse=True)
        elif sort_option == "Price (low to high)":
            return sorted(before_sort_data, key=lambda x: x["price"])
        elif sort_option == "Price (high to low)":
            return sorted(before_sort_data, key=lambda x: x["price"], reverse=True)
        else:
            raise ValueError(f"Option de tri inconnue : {sort_option}")
    
    def get_item_button(self, item_name):
        """Récupère le bouton Add to cart/Remove d'un produit."""
        items = self.find_elements_visible(self.INVENTORY_ITEMS)

        for item in items:
            name = item.find_element(*self.ITEM_NAME).text

            if name == item_name:
                return item.find_element(*self.ADD_TO_CART_BUTTON)

        raise ValueError(f"Produit introuvable : {item_name}")
    
    def add_item_to_cart(self, item_name):
        """Ajoute un produit au panier à partir de son nom."""
        button = self.get_item_button(item_name)
        
        if button.text != "Add to cart":
            raise AssertionError(f"Impossible d'ajouter : état actuel = {button.text}")
        
        button.click()
        
    def remove_item_from_cart(self, item_name):
        """Retire un produit du panier à partir de son nom."""
        button = self.get_item_button(item_name)
        
        if button.text != "Remove":
            raise AssertionError(f"Impossible de retirer : état actuel = {button.text}")
        
        button.click()
    
    def get_cart_item_count(self):
        """
        Retourne le nombre d'articles présents dans le panier.
        Retourne 0 si le badge du panier n'est pas affiché.
        """

        if not self.find_element_visible(self.CART_BADGE):
            return 0

        badge_text = self.get_text(self.CART_BADGE).strip()

        try:
            return int(badge_text)
        except ValueError:
            raise ValueError(f"Valeur invalide du badge panier : '{badge_text}'")
            
    def go_to_cart(self):
        """Clique sur l'icône du panier pour accéder à la page du panier."""
        self.click(self.CART_ICON)
        
    def is_cart_page_displayed(self):
        """Vérifie que le clic sur l'icône du panier redirige vers la page du panier."""
        return self.wait_for_url_contains("cart") and self.is_text_present(self.PAGE_TITLE, "Your Cart")
    
    def logout(self):
        """Effectue la déconnexion de l'utilisateur en utilisant le menu burger."""
        logger.info("🖱️ Cliquer sur le bouton du menu burger pour ouvrir le menu latéral")
        self.click(self.BURGER_MENU_BUTTON)
        logger.info("🖱️ Cliquer sur le lien 'LOGOUT' pour se déconnecter")
        self.click(self.LOGOUT_LINK)
        
    def is_logout_successful(self):
        """Vérifie que la déconnexion a réussi en vérifiant que l'URL correspond à celle de la page de connexion."""
        return self.wait_for_url(BASE_URL)
    