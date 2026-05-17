# ==============================
# =========== LIBRARY ==========
# ==============================

import allure
import pytest
from core.utils import get_credentials, take_screenshot
from core.logger import logger


# ==============================
# ====== TEST VALID USER =======
# ==============================

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_valid_user(login_page, driver):
    """Vérifie qu'un utilisateur avec des identifiants valides peut se connecter."""
    
    creds = get_credentials("valid_user")

    allure.dynamic.title(f"Connexion avec identifiants valides : '{creds['username']}'")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()
    
    with allure.step("Saisir les identifiants et se connecter"):
        login_page.login(creds["username"], creds["password"])
        
    with allure.step(f"Vérifier que '{creds['username']}' est connecté"):
        assert login_page.wait_inventory_page(), "Connexion K.O. Page inventaire introuvable."
    take_screenshot(driver, f"Login_Success_{creds['username']}")


# ==============================
# ====== TEST LOCKED USER ======
# ==============================


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_locked_user(login_page, driver):
    """Vérifie qu'un utilisateur bloqué ne peut pas se connecter."""
    
    creds = get_credentials("locked_user")

    allure.dynamic.title(f"Connexion avec utilisateur bloqué : '{creds['username']}'")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()
    
    with allure.step("Saisir les identifiants et tenter de se connecter"):
        login_page.login(creds["username"], creds["password"])
    
    error_message = "Sorry, this user has been locked out."
    with allure.step(f"Obtenir le message : {error_message}"):
        assert error_message in login_page.get_error_message(), (
            f"Message d'erreur incorrect.\n"
            f"Obtenu: {login_page.get_error_message()}\n"
            f"Attendu: {error_message}"
        )
    
    
# ==============================
# = TEST INVALID PASSWORD USER =
# ==============================
    

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_invalid_password(login_page, driver):
    """Vérifie qu'un utilisateur qui saisit un mot de passe incorrect ne peut pas se connecter."""
    
    creds = get_credentials("invalid_password_user")

    allure.dynamic.title(f"Connexion avec mot de passe incorrect : '{creds['username']}'")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()
    
    with allure.step("Saisir les identifiants et tenter de se connecter"):
        login_page.login(creds["username"], creds["password"])
    
    error_message = "Username and password do not match any user"
    with allure.step(f"Obtenir le message : {error_message}"):
        assert error_message in login_page.get_error_message(), (
            f"Message d'erreur incorrect.\n"
            f"Obtenu: {login_page.get_error_message()}\n"
            f"Attendu: {error_message}"
        )
    

# ==============================
# ====== TEST EMPTY USER =======
# ==============================


@allure.title("Connexion avec champs username et password vides")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_empty_fields(login_page, driver):
    """Vérifie qu'un utilisateur qui n'entre pas les informations de connexion ne peut pas se connecter."""
    
    creds = get_credentials("empty_user")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()
    
    with allure.step("Laisser Username et Password vides et tenter de se connecter"):
        login_page.login(creds["username"], creds["password"])
    
    error_message = "Username is required"
    with allure.step(f"Obtenir le message : {error_message}"):
        assert error_message in login_page.get_error_message(), (
            f"Message d'erreur incorrect.\n"
            f"Obtenu: {login_page.get_error_message()}\n"
            f"Attendu: {error_message}"
        )