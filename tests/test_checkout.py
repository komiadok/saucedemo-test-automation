# ===========================================
# ================= LIBRARY =================
# ===========================================

import allure
import pytest
from core.utils import get_credentials, get_checkout, take_screenshot


# ===========================================
# =========== TEST AFFICHAGE PAGE ===========
# ===========================================


@allure.title("Affichage de la page paiement")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.checkout
def test_checkout_page_display(logged_user, cart_page, checkout_page, driver):
    """
    Vérifie que la page paiement s'affiche correctement :
    - le formulaire de paiement est visible
    - le bouton 'Continue' est visible
    - le bouton 'Cancel' est visible
    """
    
    inventory_page = logged_user
    inventory_page.header.open_cart()
    cart_page.go_to_checkout()
    
    with allure.step("Vérifier que le formulaire de paiement est visible"):
        assert checkout_page.wait_form_elements(), "Un ou plusieurs éléments du formulaire ne sont pas visibles."
        
    with allure.step("Vérifier que le bouton 'Continue' est visible"):
        assert checkout_page.wait_continue_btn(), "Le bouton 'Continue' n'est pas visible."
        
    with allure.step("Vérifier que le bouton 'Cancel' est visible"):
        assert checkout_page.wait_cancel_btn(), "Le bouton 'Cancel' n'est pas visible."
    take_screenshot(driver, "Checkout_Page_Display")
    

# ===========================================
# ======== TEST ANNULATION PAIEMENT =========
# ===========================================


@allure.title("Annulation lors du paiement")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.checkout
def test_cancel_checkout(logged_user, cart_page, checkout_page, driver):
    """Vérifie que l'utilisateur peut annuler le paiement et revenir en arrière avant la validation."""
    
    inventory_page = logged_user
    inventory_page.header.open_cart()
    cart_page.go_to_checkout()
    
    with allure.step("Cliquer sur le bouton 'Cancel'"):
        checkout_page.cancel_checkout()
        
    with allure.step("Vérifier que l'utilisateur revient sur la page panier"):
        assert checkout_page.wait_cart_page(), "L'utilisateur n'est pas sur la page panier."
        

# ===========================================
# = TEST VALIDATION FORMULAIRE DE PAIEMENT ==
# ===========================================


@allure.title("Validation du formulaire de paiement")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.checkout
def test_validate_checkout_form(logged_user, cart_page, checkout_page, driver):
    """Vérifie que l'utilisateur peut valider le formulaire de paiement avec des informations valides."""
    
    inventory_page = logged_user
    inventory_page.header.open_cart()
    cart_page.go_to_checkout()
    
    ck = get_checkout("standard_user")
    
    with allure.step("Remplir le formulaire et valider"):
        checkout_page.validate_checkout_form(ck["first_name"], ck["last_name"], ck["zip_code"])
        
    with allure.step("Vérifier que l'utilisateur passe à la seconde étape du paiement"):
        assert checkout_page.wait_checkout_step_two(), "Erreur: Paiment interrompu. Page 'checkout-step-two' introuvable."
    take_screenshot(driver, "Checkout_Step_Two_Page")
    

# ===========================================
# ==== TEST CONTRÔLE PRIX RÉCAPITULATIF =====
# ===========================================


@allure.title("Contrôle du prix total dans le récapitulatif")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.checkout
def test_total_price_control(logged_user, cart_page, checkout_page, driver):
    """Vérifie que le prix total du produit affiché dans le récapitulatif est correct."""

    inventory_page = logged_user
    inventory_page.add_item_to_cart("Sauce Labs Backpack")
    inventory_page.header.open_cart()
    cart_page.go_to_checkout()
    
    ck = get_checkout("standard_user")
    checkout_page.validate_checkout_form(ck["first_name"], ck["last_name"], ck["zip_code"])

    expected_price = checkout_page.calculate_total_price()
    received_price = checkout_page.get_total_price()
        
    with allure.step(f"Vérifier que le prix affiché dans le récapitulatif est ${expected_price}"):
        assert received_price == expected_price, f"Prix total incorrect.\nAttendu: {expected_price}\nObtenu: {received_price}."
    take_screenshot(driver, "Total_Price_Correct")


# ===========================================
# ====== TEST CONFIRMATION DE PAIEMENT ======
# ===========================================


@allure.title("Confirmation de paiement")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.checkout
def test_confirm_checkout(logged_user, cart_page, checkout_page, driver):
    """Vérifie que l'utilisateur peut confirmer le paiement."""
    
    inventory_page = logged_user
    inventory_page.header.open_cart()
    cart_page.go_to_checkout()
    
    ck = get_checkout("standard_user")
    checkout_page.validate_checkout_form(ck["first_name"], ck["last_name"], ck["zip_code"])
    
    with allure.step("Cliquer sur le bouton 'Finish'"):
        checkout_page.confirm_checkout()
        
    with allure.step("Vérifier le succès du paiement"):
        assert "Thank you for your order!" in checkout_page.get_checkout_sucess_message(), (
            f"Le message obtenu n'est pas celui attendu.\n"
            f"Attendu: Thank you for your order!\n"
            f"Obtenu: {checkout_page.get_checkout_sucess_message()}"
        )
        assert checkout_page.wait_back_home_btn(), "Le bouton 'Back Home' est introuvable."
    take_screenshot(driver, "Checkout_Success")


# ===========================================
# ======== PARCOURS D'ACHAT COMPLET =========
# ===========================================


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.e2e
def test_complete_purchase(login_page, inventory_page, cart_page, checkout_page, driver):
    """Vérifie que l'utilisateur peut réaliser un parcours d'achat complet de l'inscription au paiement."""
    
    creds = get_credentials("valid_user")

    allure.dynamic.title(f"Parcours d'achat complet pour l'utilisateur '{creds['username']}'")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()
    
    with allure.step("Saisir les identifiants et se connecter"):
        login_page.login(creds["username"], creds["password"])
        
    item_name = "Sauce Labs Backpack"
    with allure.step(f"Ajouter le produit '{item_name}' au panier."):
        inventory_page.add_item_to_cart(item_name)
        
    with allure.step("Accéder au panier"):    
        inventory_page.header.open_cart()
        
    with allure.step("Cliquer sur le bouton 'Checkout'"):
        cart_page.go_to_checkout()
        
    ck = get_checkout("standard_user")
    with allure.step("Remplir le formulaire et valider"):
        checkout_page.validate_checkout_form(ck["first_name"], ck["last_name"], ck["zip_code"])
        
    with allure.step("Confirmer le paiement"):
        checkout_page.confirm_checkout()
        
    with allure.step("Vérifier le succès du paiement"):
        assert "Thank you for your order!" in checkout_page.get_checkout_sucess_message(), (
            f"Le message obtenu n'est pas celui attendu.\n"
            f"Attendu: Thank you for your order!\n"
            f"Obtenu: {checkout_page.get_checkout_sucess_message()}"
        )
        assert checkout_page.wait_back_home_btn(), "Le bouton 'Back Home' est introuvable."
    take_screenshot(driver, "Complete_Purchase_Success")