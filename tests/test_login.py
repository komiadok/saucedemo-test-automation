import pytest
import allure

from core.logger import logger
from core.utils import get_credentials, take_screenshot
from pages.login_page import LoginPage

@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_success(driver):
    
    login_page = LoginPage(driver)
    
    valid_user = get_credentials("valid_user")
    username = valid_user["username"]
    password = valid_user["password"]
    
    allure.dynamic.title(f"Connexion réussie pour {username}")
    
    logger.info(f"🚀 Début test de connexion pour {username}")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()

    with allure.step("Saisir les identifiants et se connecter"):
        login_page.login(username, password)

    with allure.step("Vérifier que la connexion a réussi"):
        assert login_page.is_login_successful()
        logger.info(f"➜ Redirection réussie vers la page d'inventaire après connexion pour {username}")
        take_screenshot(driver, f"Login_Success_{username}")

    logger.info(f"✅ Test de connexion réussi pour l'utilisateur : {username}")


@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_failure_locked_user(driver):
    
    login_page = LoginPage(driver)
    
    locked_user = get_credentials("locked_user")
    username = locked_user["username"]
    password = locked_user["password"]
    
    allure.dynamic.title(f"Connexion échouée pour {username}")
    
    logger.info(f"🚀 Début test de connexion pour {username}")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()

    with allure.step("Saisir les identifiants et tenter de se connecter"):
        login_page.login(username, password)

    with allure.step("Vérifier que le message d'erreur est affiché et correct"):
        assert login_page.is_error_message_displayed()
        error_message = login_page.get_error_message()
        logger.info(f"📩 Message d'erreur affiché : {error_message}")
        
        expected_message = "Sorry, this user has been locked out."
        assert login_page.is_error_message_valid(expected_message), (
            f"Message d'erreur incorrect.\nAttendu : {expected_message}\nObtenu : {error_message}"
        )

    logger.info(f"✅ Test de connexion échoué pour l'utilisateur bloqué : {username}")
    
    
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_failure_invalid_password(driver): 
    
    login_page = LoginPage(driver)
    
    invalid_user = get_credentials("invalid_password_user")
    username = invalid_user["username"]
    password = invalid_user["password"]
    
    allure.dynamic.title(f"Connexion échouée pour {username}")
    
    logger.info(f"🚀 Début test de connexion pour {username}")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()

    with allure.step("Saisir les identifiants et tenter de se connecter"):
        login_page.login(username, password)

    with allure.step("Vérifier que le message d'erreur est affiché et correct"):
        assert login_page.is_error_message_displayed()
        error_message = login_page.get_error_message()
        logger.info(f"📩 Message d'erreur affiché : {error_message}")
        
        expected_message = "Username and password do not match any user"
        assert login_page.is_error_message_valid(expected_message), (
            f"Message d'erreur incorrect.\nAttendu : {expected_message}\nObtenu : {error_message}"
        )

    logger.info(f"✅ Test de connexion avec mot de passe invalide échoué pour l'utilisateur : {username}")
    
    
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.smoke
@pytest.mark.login
def test_login_failure_empty_credentials(driver): 
    
    login_page = LoginPage(driver)
    
    empty_user = get_credentials("empty_user")
    username = empty_user["username"]
    password = empty_user["password"]
    
    allure.title("Connexion échouée avec des champs vides")
    
    logger.info(f"🚀 Début test de connexion pour {username}")
    
    with allure.step("Ouvrir la page de connexion"):
        login_page.open_login_page()

    with allure.step("Laisser les champs 'Username' et 'Password' vides et tenter de se connecter"):
        login_page.login(username, password)

    with allure.step("Vérifier que le message d'erreur est affiché et correct"):
        assert login_page.is_error_message_displayed()
        error_message = login_page.get_error_message()
        logger.info(f"📩 Message d'erreur affiché : {error_message}")
        
        expected_message = "Username is required"
        assert login_page.is_error_message_valid(expected_message), (
            f"Message d'erreur incorrect.\nAttendu : {expected_message}\nObtenu : {error_message}"
        )

    logger.info("✅ Test de connexion avec identifiants vides échoué.")