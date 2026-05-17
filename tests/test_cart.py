# ===========================================
# ================= LIBRARY =================
# ===========================================

import allure
import pytest
from core.utils import take_screenshot


# ===========================================
# =========== TEST AFFICHAGE PAGE ===========
# ===========================================


@allure.title("Affichage de la page panier")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.cart
def test_cart_page_display(logged_user, cart_page, driver):
    """
    Vérifie que la page panier s'affiche correctement :
    - le bouton 'Checkout' est visible
    - le bouton 'Continue Shopping' est visible
    """
    
    inventory_page = logged_user
    inventory_page.header.open_cart()
    
    with allure.step("Vérifier que le bouton 'Checkout' est présent"):
        assert cart_page.wait_checkout_btn(), "Le bouton 'Checkout' est introuvable."
        
    with allure.step("Vérifier que le bouton 'Continue Shopping' est présent"):
        assert cart_page.wait_continue_shopping_btn(), "Le bouton 'Continue Shopping' est introuvable."
        

# ===========================================
# ========== TEST CONTINUE SHOPPING =========
# ===========================================


@allure.title("Accès à la page inventaire depuis le panier")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.cart
def test_continue_shopping(logged_user, cart_page, driver):
    """Vérifie que l'utilisateur peut revenir sur la page inventaire depuis la page panier"""
    
    inventory_page = logged_user
    inventory_page.header.open_cart()
    
    with allure.step("Cliquer sur le bouton 'Continue Shopping'"):
        cart_page.continue_shopping()
        
    with allure.step("Vérifier que l'utilisateur est redirigé sur la page inventaire"):
        cart_page.wait_inventory_page()
    take_screenshot(driver, "Inventory_Page_Display")
    

# ===========================================
# ============= TEST REMOVE ITEM ============
# ===========================================


@allure.title("Suppression d'un produit depuis le panier")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.cart
def test_remove_item_from_cart_page(logged_user, cart_page, driver):
    """Vérifie que l'utilisateur peut retirer un produit depuis la page panier"""
    
    inventory_page = logged_user
    
    item_name = "Sauce Labs Backpack"
    with allure.step(f"Ajouter le produit '{item_name}' au panier."):
        inventory_page.add_item_to_cart(item_name)
        
    with allure.step("Accéder au panier"):    
        inventory_page.header.open_cart()
    
    with allure.step(f"Retirer le produit '{item_name}' du panier"):
        cart_page.remove_item_from_cart(item_name)
    
    with allure.step(f"Vérifier que le produit '{item_name}' n'est plus présent sur la page"):
        assert cart_page.wait_item_disappeared(item_name), f"'{item_name}' est toujours présent sur la page"
    take_screenshot(driver, f"{item_name}_Disappeared_From_Cart")
    

# ===========================================
# ============= TEST CART ITEMS =============
# ===========================================


@allure.title("Vérification des produits ajoutés par l'utilisateur")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.cart
def test_cart_contains_added_items(logged_user, cart_page, driver):
    """Vérifie que les produits dans le panier correspondent aux produits ajoutés par l'utilisateur."""
    
    inventory_page = logged_user
    
    items_to_add = [
        "Sauce Labs Backpack",
        "Sauce Labs Bolt T-Shirt"
    ]
    
    with allure.step(f"Ajouter les produits '{items_to_add[0]}' et '{items_to_add[1]}' au panier"):
        for item in items_to_add:
            inventory_page.add_item_to_cart(item)
    
    with allure.step("Accéder au panier"):    
        inventory_page.header.open_cart()
        
    with allure.step(f"Vérifier qu'il y a {len(items_to_add)} produits dans le panier"):
        cart_items = cart_page.get_item_names()
        assert len(cart_items) == len(items_to_add), (
            f"Nombre de produits incorrect.\n"
            f"Attendu: {len(items_to_add)}\n"
            f"Obtenu: {len(cart_items)}"
        )
        
    with allure.step(f"Vérifier que les produits ajoutés dans le panier sont : '{items_to_add[0]}' et '{items_to_add[1]}'"):
        assert set(items_to_add) == set(cart_items), (
            f"Les produits du panier ne correspondent pas.\n"
            f"Attendu: {items_to_add}\n"
            f"Obtenu: {cart_items}"
        )
    take_screenshot(driver, "Added_Items_Control")
    
    
# ===========================================
# ============== TEST CHECKOUT ==============
# ===========================================


@allure.title("Accès à la page checkout")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.cart
def test_go_to_checkout(logged_user, cart_page, driver):
    """Vérifie que l'utilisateur peut accéder à la page de checkout."""
    
    inventory_page = logged_user
    inventory_page.header.open_cart()
    
    with allure.step("Cliquer sur le bouton 'Checkout'"):
        cart_page.go_to_checkout()
        
    with allure.step("Vérifier que la page de checkout s'ouvre"):
        cart_page.wait_checkout_page()
    take_screenshot(driver, "Checkout_Step_One_Page_Display")
    