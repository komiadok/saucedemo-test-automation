# ==============================
# ========== LIBRARY ===========
# ==============================

import pytest
from core.utils import get_credentials, take_screenshot
from core.driver_factory import create_driver
from pages.login_page import LoginPage
from pages.inventory_page import InventoryPage
from pages.cart_page import CartPage


# ==============================
# ========== FIXTURES ==========
# ==============================

@pytest.fixture
def driver():
    """Initialise et ferme le WebDriver Selenium."""
    driver = create_driver()
    yield driver
    driver.quit()


@pytest.fixture
def login_page(driver):
    """Retourne une instance de la page Login."""
    return LoginPage(driver)


@pytest.fixture
def inventory_page(driver):
    """Retourne une instance de la page Inventory."""
    return InventoryPage(driver)


@pytest.fixture
def cart_page(driver):
    """Retourne une instance de la page Cart."""
    return CartPage(driver)


@pytest.fixture
def logged_user(driver, login_page, inventory_page):
    """Connecte un utilisateur valide et retourne la page Inventory."""
    creds = get_credentials("valid_user")

    login_page.open_page()
    login_page.login(creds["username"], creds["password"])
    login_page.wait_inventory_page()

    return inventory_page


# ==============================
# ============ HOOKS ===========
# ==============================

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook exécuté après chaque phase de test.
    Capture automatiquement une screenshot en cas d'échec.
    """
    outcome = yield
    result = outcome.get_result()

    if result.when != "call":
        return

    if result.failed:
        driver = item.funcargs.get("driver")

        if driver:
            try:
                path = take_screenshot(driver, f"FAILED_{item.name}")
            except Exception as e:
                pass





