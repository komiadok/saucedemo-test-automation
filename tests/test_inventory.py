import pytest
import allure

from core.logger import logger
from core.utils import get_credentials, take_screenshot

from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage

@allure.title("Vérification de l'affichage de la page d'inventaire")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
def test_inventory_page_displayed(driver):
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    valid_user = get_credentials("valid_user")
    username = valid_user["username"]
    password = valid_user["password"]
    
    logger.info("🚀 Début du test de vérification de l'affichage de la page d'inventaire")
    
    with allure.step("Se connecter avec des identifiants valides"):
        login_page.open_login_page()
        login_page.login(username, password)
        logger.info("✅ Connexion réussie pour l'utilisateur : {username}")
    
    logger.info("🔍 Vérification de l'affichage de la page d'inventaire")
    
    expected_page_title = "Products"
    with allure.step(f"Vérifier que le titre de la page d'inventaire affiché est '{expected_page_title}'"):
        assert inventory_page.is_page_title_displayed(), "Le titre de la page d'inventaire n'est pas affiché."
        inventory_page_title = inventory_page.get_page_title()
        assert inventory_page.is_page_title_correct(expected_page_title), (
            f"Le titre de la page d'inventaire est incorrect.\nAttendu : {expected_page_title}\nObtenu : {inventory_page_title}"
        )
        logger.info(f"📌 Titre de la page d'inventaire affiché : {inventory_page_title}")
        
    with allure.step("Vérifier que l'icône du panier est présente sur la page d'inventaire"):
        assert inventory_page.is_cart_icon_displayed(), "L'icône du panier n'est pas présente sur la page d'inventaire."
        logger.info("📌 L'icône du panier est présente sur la page d'inventaire.")    
      
    with allure.step("Vérifier que le bouton du menu burger est présent sur la page d'inventaire"):
        assert inventory_page.is_burger_menu_displayed(), "Le bouton du menu burger n'est pas présent sur la page d'inventaire."
        logger.info("📌 Le bouton du menu burger est présent sur la page d'inventaire.")
     
    with allure.step("Vérifier que le dropdown de tri est présent sur la page d'inventaire"):
        assert inventory_page.is_sort_dropdown_displayed(), "Le dropdown de tri n'est pas présent sur la page d'inventaire."
        logger.info("📌 Le dropdown de tri est présent sur la page d'inventaire.")
      
    expected_items_count = 6
    with allure.step(f"Vérifier que la page d'inventaire affiche {expected_items_count} produits"):
        assert inventory_page.is_inventory_items_displayed(), "Les produits ne sont pas affichés sur la page d'inventaire."
        actual_items_count = inventory_page.get_inventory_items_count()
        assert actual_items_count == expected_items_count, (
            f"Le nombre de produits affichés est incorrect.\nAttendu : {expected_items_count}\nObtenu : {actual_items_count}"
        )
        logger.info(f"📌 Nombre de produits affichés sur la page d'inventaire : {actual_items_count}")
    
    with allure.step("Vérifier que les produits affichés sur la page d'inventaire comportent un nom, un prix et un bouton 'Add to cart'"): 
        assert inventory_page.are_all_inventory_items_valid(), "Un ou plusieurs produits affichés ne sont pas valides."
        logger.info("📌 Tous les produits affichés sur la page d'inventaire comportent un nom, un prix et un bouton 'Add to cart'.")
        
    take_screenshot(driver, "Inventory_Page_Display")
    
    logger.info("✅ La page d'inventaire est correctement affichée.")

    
@allure.title("Vérification de l'affichage des produits après tri dans la page d'inventaire")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
def test_inventory_sorting_functionality(driver):
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    valid_user = get_credentials("valid_user")
    username = valid_user["username"]
    password = valid_user["password"]
    
    logger.info("🚀 Début du test de vérification de l'affichage des produits après tri dans la page d'inventaire")
    
    with allure.step("Se connecter avec des identifiants valides"):
        login_page.open_login_page()
        login_page.login(username, password)
        logger.info(f"✅ Connexion réussie pour l'utilisateur : {username}")
    
    selected_sort_option = "Name (Z to A)"
    with allure.step(f"Vérifier que le dropdown de tri fonctionne correctement en sélectionnant l'option '{selected_sort_option}'"):
        items_order_before_sorting = inventory_page.extract_items_order()
        logger.info(f"🔍 Ordre d'apparition des produits avant tri : {items_order_before_sorting}")
        take_screenshot(driver, f"Inventory_Items_Order_Before_Sorting_{selected_sort_option}")
        
        logger.info(f"📌 Sélection de l'option de tri : '{selected_sort_option}'")
        inventory_page.select_sort_option(selected_sort_option)
        
        items_order_after_sorting = inventory_page.extract_items_order()
        logger.info(f"🔍 Ordre d'apparition des produits après tri : {items_order_after_sorting}")
        
        expected_sorted_order = inventory_page.get_expected_sorted_items_order(items_order_before_sorting, selected_sort_option)
        assert items_order_after_sorting == expected_sorted_order, (
            f"L'ordre des produits après tri est incorrect pour l'option '{selected_sort_option}'.\n"
            f"Attendu : {expected_sorted_order}\n"
            f"Obtenu : {items_order_after_sorting}"
        )
        take_screenshot(driver, f"Inventory_Items_Order_After_Sorting_{selected_sort_option}")
        logger.info(f"✅ Le dropdown de tri fonctionne correctement avec l'option '{selected_sort_option}'.")
    
    selected_sort_option = "Name (A to Z)"
    with allure.step(f"Vérifier que le dropdown de tri fonctionne correctement en sélectionnant l'option '{selected_sort_option}'"):
        items_order_before_sorting = inventory_page.extract_items_order()
        
        logger.info(f"📌 Sélection de l'option de tri : '{selected_sort_option}'")
        inventory_page.select_sort_option(selected_sort_option)
        
        items_order_after_sorting = inventory_page.extract_items_order()
        logger.info(f"🔍 Ordre d'apparition des produits après tri : {items_order_after_sorting}")
        
        expected_sorted_order = inventory_page.get_expected_sorted_items_order(items_order_before_sorting, selected_sort_option)
        assert items_order_after_sorting == expected_sorted_order, (
            f"L'ordre des produits après tri est incorrect pour l'option '{selected_sort_option}'.\n"
            f"Attendu : {expected_sorted_order}\n"
            f"Obtenu : {items_order_after_sorting}"
        )
        take_screenshot(driver, f"Inventory_Items_Order_After_Sorting_{selected_sort_option}")
        logger.info(f"✅ Le dropdown de tri fonctionne correctement avec l'option '{selected_sort_option}'.")
        
    selected_sort_option = "Price (low to high)"
    with allure.step(f"Vérifier que le dropdown de tri fonctionne correctement en sélectionnant l'option '{selected_sort_option}'"):
        items_order_before_sorting = inventory_page.extract_items_order()
        
        logger.info(f"📌 Sélection de l'option de tri : '{selected_sort_option}'")
        inventory_page.select_sort_option(selected_sort_option)
        
        items_order_after_sorting = inventory_page.extract_items_order()
        logger.info(f"🔍 Ordre d'apparition des produits après tri : {items_order_after_sorting}")
        
        expected_sorted_order = inventory_page.get_expected_sorted_items_order(items_order_before_sorting, selected_sort_option)
        assert items_order_after_sorting == expected_sorted_order, (
            f"L'ordre des produits après tri est incorrect pour l'option '{selected_sort_option}'.\n"
            f"Attendu : {expected_sorted_order}\n"
            f"Obtenu : {items_order_after_sorting}"
        )
        take_screenshot(driver, f"Inventory_Items_Order_After_Sorting_{selected_sort_option}")
        logger.info(f"✅ Le dropdown de tri fonctionne correctement avec l'option '{selected_sort_option}'.")
    
    selected_sort_option = "Price (high to low)"
    with allure.step(f"Vérifier que le dropdown de tri fonctionne correctement en sélectionnant l'option '{selected_sort_option}'"):
        items_order_before_sorting = inventory_page.extract_items_order()
        
        logger.info(f"📌 Sélection de l'option de tri : '{selected_sort_option}'")
        inventory_page.select_sort_option(selected_sort_option)
        
        items_order_after_sorting = inventory_page.extract_items_order()
        logger.info(f"🔍 Ordre d'apparition des produits après tri : {items_order_after_sorting}")
        
        expected_sorted_order = inventory_page.get_expected_sorted_items_order(items_order_before_sorting, selected_sort_option)
        assert items_order_after_sorting == expected_sorted_order, (
            f"L'ordre des produits après tri est incorrect pour l'option '{selected_sort_option}'.\n"
            f"Attendu : {expected_sorted_order}\n"
            f"Obtenu : {items_order_after_sorting}"
        )
        take_screenshot(driver, f"Inventory_Items_Order_After_Sorting_{selected_sort_option}")
        logger.info(f"✅ Le dropdown de tri fonctionne correctement avec l'option '{selected_sort_option}'.")
        
    logger.info("✅ Le dropdown de tri fonctionne correctement pour toutes les options de tri testées.")

    
@allure.title("Ajout et suppression de produits dans le panier")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
def test_add_remove_items(driver):
    """Vérifie que l'utilisateur peut ajouter et supprimer un article du panier depuis la page inventaire."""
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    valid_user = get_credentials("valid_user")
    username = valid_user["username"]
    password = valid_user["password"]
    
    logger.info("🚀 Début du test d'ajout et de suppression de produits dans le panier depuis la page d'inventaire")
    
    with allure.step("Se connecter avec des identifiants valides"):
        login_page.open_login_page()
        login_page.login(username, password)
        logger.info(f"✅ Connexion réussie pour l'utilisateur : {username}")
    
    item1_to_add = "Sauce Labs Backpack"
    item2_to_add = "Sauce Labs Bolt T-Shirt"
    with allure.step(f"Ajouter les produits '{item1_to_add}' et '{item2_to_add}' au panier"):
        inventory_page.add_item_to_cart(item1_to_add)
        logger.info(f"🛒 '{item1_to_add}' ajouté au panier")
    
        inventory_page.add_item_to_cart(item2_to_add)
        logger.info(f"🛒 '{item2_to_add}' ajouté au panier")
    
    with allure.step(f"Retirer le produit '{item1_to_add}' du panier"):
        inventory_page.remove_item_from_cart(item1_to_add)
        logger.info(f"🗑️ '{item1_to_add}' retiré du panier")
    
    expected_cart_item_count = 1
    with allure.step(f"Vérifier que le badge du panier affiche {expected_cart_item_count}"):
        cart_item_count = inventory_page.get_cart_item_count()
        assert cart_item_count == expected_cart_item_count, (
            f"Le nombre affiché par le badge du panier est incorrect.\n"
            f"Attendu : {expected_cart_item_count}\n"
            f"Obtenu : {cart_item_count}"
        )
        take_screenshot(driver, "Add_Remove_Items_Success")
        
    logger.info(f"✅ Test d'ajout et de suppresion de produits depuis la page inventaire réussi.")


@allure.title("Redirection vers le panier depuis la page inventaire.")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
@pytest.mark.cart
def test_go_to_cart(driver):
    """Vérifie que l'utilisateur est redirigé vers le panier en cliquant sur l'icône du panier depuis la page inventaire."""
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    valid_user = get_credentials("valid_user")
    username = valid_user["username"]
    password = valid_user["password"]
    
    logger.info("🚀 Début du test de redirection vers le panier depuis la page d'inventaire")
    
    with allure.step("Se connecter avec des identifiants valides"):
        login_page.open_login_page()
        login_page.login(username, password)
        logger.info(f"✅ Connexion réussie pour l'utilisateur : {username}")
        
    with allure.step("Cliquer sur l'icône du panier"):
        inventory_page.go_to_cart()
        logger.info("➜ Tentative de redirection vers le panier")
        
        assert inventory_page.is_cart_page_displayed(), "La redirection vers le panier a échoué.\nLes éléments attendus ne sont pas affichés."
        take_screenshot(driver, "Go_to_cart_Success")
    
    logger.info("✅ Test de redirection vers le panier depuis la page inventaire réussi.")

@allure.title("Déconnexion de la page d'inventaire")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.inventory
@pytest.mark.logout
def test_logout(driver):
    """Vérifie que l'utilisateur peut se déconnecter depuis la page d'inventaire."""
    
    login_page = LoginPage(driver)
    inventory_page = InventoryPage(driver)
    
    valid_user = get_credentials("valid_user")
    username = valid_user["username"]
    password = valid_user["password"]
    
    logger.info("🚀 Début du test de déconnexion depuis la page d'inventaire")
    
    with allure.step("Se connecter avec des identifiants valides"):
        login_page.open_login_page()
        login_page.login(username, password)
        logger.info(f"✅ Connexion réussie pour l'utilisateur : {username}")
    
    with allure.step("Effectuer la déconnexion depuis la page d'inventaire"):
        inventory_page.logout()
        logger.info("🔓 Tentative de déconnexion.")
        
    with allure.step("Vérifier que l'utilisateur est redirigé vers la page de connexion après la déconnexion"):
        assert inventory_page.is_logout_successful(), "L'utilisateur n'est pas redirigé vers la page de connexion après la déconnexion."
        logger.info("➜ L'utilisateur est redirigé vers la page de connexion")
        
    take_screenshot(driver, "Logout_From_Inventory_Page")
    
    logger.info(f"✅ Déconnexion réussie pour l'utilisateur : {username}")
    