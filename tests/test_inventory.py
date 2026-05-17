# ===========================================
# ================= LIBRARY =================
# ===========================================

import allure
import pytest
from core.utils import take_screenshot


# ===========================================
# =========== TEST AFFICHAGE PAGE ===========
# ===========================================


@allure.title("Affichage de la page inventaire")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
def test_inventory_page_display(logged_user, driver):
    """
    Vérifie que la page inventaire s'affiche correctement :
    - l'icône du panier est visible
    - le menu latéral est visible
    - le dropdown de tri est visible
    - 6 produits sont visibles
    - Chaque produit a un nom, un prix et un bouton 'Add to cart'
    """
    
    inventory_page = logged_user
    
    with allure.step("Vérifier que l'icône du panier s'affiche"):
        assert inventory_page.header.wait_cart_icon(), "L'icône du panier est introuvable."
        
    with allure.step("Vérifier que le menu latéral s'affiche"):
        assert inventory_page.header.wait_menu_btn(), "Le menu latéral est introuvable."
        
    with allure.step("Vérifier que le dropdown de tri s'affiche"):
        assert inventory_page.wait_sort_dropdown(), "Le dropdown de tri est introuvable."
    
    items_count = 6
    with allure.step(f"Vérifier que {items_count} produits sont visibles"):
        assert len(inventory_page.get_items_data()) == items_count, "Le nombre de produits affiché est incorrect."
        
    with allure.step("Vérifier que chaque produit a un nom, un prix et un bouton 'Add to cart'"):
        assert all(inventory_page.wait_item_elements_visible()), "Un ou plusieurs éléments manquent pour des produits."
    take_screenshot(driver, "Inventory_Page_Display")


# ===========================================
# ========== TEST TRI DES PRODUITS ==========
# ===========================================


@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.inventory
@pytest.mark.parametrize("sort_option", ["Name (A to Z)", "Name (Z to A)", "Price (low to high)", "Price (high to low)"])
def test_inventory_page_sort(logged_user, driver, sort_option):
    """Vérifie que le tri s'applique correctement aux produits de la page."""
    
    inventory_page = logged_user
    
    allure.dynamic.title(f"Tri des produits - {sort_option}")
    
    with allure.step("Récupérer l'ordre des produits avant tri"):
        before_sort = inventory_page.get_items_data()
    
    with allure.step(f"Appliquer le tri : {sort_option}"):
        inventory_page.select_sort(sort_option)
        
    with allure.step("Récupérer l'ordre des produits après tri"):
        after_sort = inventory_page.get_items_data()
    
    with allure.step("Calculer l'ordre attendu"):
        expected_sort = inventory_page.sort_items(before_sort, sort_option)
        
    with allure.step("Vérifier que le tri est correct"):
        assert after_sort == expected_sort, (
            f"Tri incorrect pour {sort_option}\n"
            f"Attendu : {expected_sort}\n"
            f"Obtenu : {after_sort}"
        )
    take_screenshot(driver, f"Inventory_Sort_{sort_option}")
    

# ===========================================
# ==== TEST AJOUT / SUPPRESSION PRODUITS ====
# ===========================================


@allure.title("Ajout et suppression de produits")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
def test_add_remove_items(logged_user, driver):
    """Vérifie que l'utilisateur peut ajouter et supprimer un article du panier depuis la page inventaire."""
    
    inventory_page = logged_user
    
    item1_name = "Sauce Labs Backpack"
    item2_name = "Sauce Labs Bolt T-Shirt"
    with allure.step(f"Ajouter les produits '{item1_name}' et '{item2_name}' au panier."):
        inventory_page.add_item_to_cart(item1_name)
        inventory_page.add_item_to_cart(item2_name)
        
    with allure.step(f"Retirer le produit '{item1_name}' du panier."):
        inventory_page.remove_item(item1_name)
        
    item_count = 1
    with allure.step(f"Vérifier que le badge du panier affiche {item_count}"):
        assert inventory_page.get_cart_count() == item_count, "Le nombre affiché par le badge est incorrect."
    take_screenshot(driver, "Add_Remove_Item")
        
    
# ===========================================
# ========== TEST ACCÈS AU PANIER ===========
# ===========================================    
        
        
@allure.title("Accès au panier depuis la page inventaire")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
def test_go_to_cart(logged_user, driver):
    """Vérifie que l'utilisateur peut accéder au panier depuis la page inventaire"""
    
    inventory_page = logged_user
    
    with allure.step("Cliquer sur l'icône du panier"):
        inventory_page.header.open_cart(), "Impossible de cliquer sur l'icône du panier"
        
    with allure.step("Vérifier que la page du panier apparaît"):
        assert inventory_page.wait_cart_page(), (
            f"L'URL ne correspond pas à la page du panier : {inventory_page.get_current_url()}"
        )
    take_screenshot(driver, "Cart_Page_Display")
    

# ===========================================
# ============ TEST DÉCONNEXION =============
# ===========================================


@allure.title("Déconnexion")
@allure.severity(allure.severity_level.NORMAL)
@pytest.mark.smoke
@pytest.mark.inventory
def test_logout(logged_user, driver):
    """Vérifie que l'utilisateur peut se déconnecter."""
    
    inventory_page = logged_user
    
    with allure.step("Cliquer sur le bouton Menu"):
        inventory_page.header.open_menu()
        
    with allure.step("Cliquer sur le bouton 'Logout'"):
        inventory_page.header.logout()
        
    with allure.step("Vérifier que l'utilisateur est sur la page de connexion"):
        inventory_page.wait_login_page()
    take_screenshot(driver, "Login_Page_Display")