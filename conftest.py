import pytest
from core.driver_factory import create_driver
from core.utils import take_screenshot
from core.logger import logger

@pytest.fixture
def browser():
    """Fixture principale Selenium WebDriver."""
    logger.info("🌐 Initialisation du navigateur")

    driver = create_driver()

    yield driver

    logger.info("🛑 Fermeture du navigateur")
    driver.quit()
            
@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
    """
    Hook exécuté après chaque phase de test.
    Capture screenshot uniquement en cas d'échec.
    """

    outcome = yield
    result = outcome.get_result()

    # On ne traite que la phase d'exécution du test
    if result.when != "call":
        return

    if result.failed:
        logger.error(f"❌ TEST FAILED : {item.name}")

        driver = item.funcargs.get("browser")

        if driver:
            try:
                path = take_screenshot(driver, f"FAILED_{item.name}")
                logger.error(f"📸 Screenshot saved: {path}")
            except Exception as e:
                logger.error(f"⚠️ Screenshot failed: {e}")