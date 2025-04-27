from typing import Dict, Generator

import pytest
from playwright.sync_api import Browser, BrowserType, Page, sync_playwright

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.Common import Common
from utils.DatabaseManager import DatabaseManager
from utils.logger import log_allure
from utils.ReadFile import ReadFile
from utils.SetDotEnv import SetDotEnv
from utils.url_helper import set_pytest_config

CONFIG_YAML_PATH = "./config.yaml"


@pytest.fixture(scope="session")
def playwright_instance():
    """Fixture para gerenciar a instância do Playwright"""
    playwright = sync_playwright().start()
    yield playwright
    playwright.stop()


@pytest.fixture(scope="session")
def browser_type(request, playwright_instance) -> BrowserType:
    """Fixture para selecionar o tipo de navegador"""
    # Obtém a opção --browser, garantindo que seja uma string
    browser_option = request.config.getoption("--browser")

    # Define o navegador padrão como 'chromium' se não for especificado
    browser_name = "chromium"

    if browser_option:
        # Se for uma lista, pega o primeiro elemento
        if isinstance(browser_option, list):
            browser_name = browser_option[0].lower()
        else:
            browser_name = str(browser_option).lower()

    # Mapeamento dos navegadores suportados
    browser_map = {
        "chromium": playwright_instance.chromium,
        "firefox": playwright_instance.firefox,
        "webkit": playwright_instance.webkit,
    }

    # Verifica se o navegador solicitado é suportado
    if browser_name not in browser_map:
        raise ValueError(
            f"Navegador '{browser_name}' não é suportado. "
            f"Opções válidas: {list(browser_map.keys())}"
        )

    return browser_map[browser_name]


@pytest.fixture(scope="session")
def browser(browser_type, is_headless) -> Generator[Browser, None, None]:
    """Fixture principal do Playwright com suporte a headless mode"""
    headless = (
        is_headless.lower() == "true"
        if isinstance(is_headless, str)
        else bool(is_headless)
    )

    browser = browser_type.launch(
        headless=headless,
        args=["--disable-gpu", "--no-sandbox"],
        slow_mo=100 if not headless else 0,
    )
    yield browser
    browser.close()


@pytest.fixture(scope="session", autouse=True)
def get_config() -> Dict:
    """Retorna as configurações do arquivo config.yaml"""
    read_file = ReadFile()
    return read_file.load_yaml_file(CONFIG_YAML_PATH)


def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Execution environment: rc, uat")
    parser.addoption(
        "--pipeline", action="store", help="Run tests in pipeline: true, false"
    )
    parser.addoption(
        "--headless", action="store", help="Run tests in headless mode: true, false"
    )


def pytest_configure(config):
    """Configure pytest"""
    set_pytest_config(config)


@pytest.fixture(scope="session", autouse=True)
def env(request, get_config):

    env_option = request.config.getoption("--env", default=None)
    if env_option:
        log_allure(f"Select environment by terminal: ENVIRONMENT {env_option.upper()}")
        return env_option

    log_allure(
        f'Select environment by config file -> {CONFIG_YAML_PATH}: ENVIRONMENT {get_config["ENVIRONMENT"]}'
    )
    return get_config["ENVIRONMENT"]


@pytest.fixture(scope="session", autouse=True)
def is_pipeline(request, get_config):

    pipeline_option = request.config.getoption("--pipeline", default=None)
    if pipeline_option:
        log_allure(
            f"Select pipeline execution by terminal: PIPELINE {pipeline_option.upper()}"
        )
        return pipeline_option

    log_allure(
        f'Select pipeline execution by config file -> {CONFIG_YAML_PATH}: PIPELINE {get_config["PIPELINE"]}'
    )
    return get_config["PIPELINE"]


@pytest.fixture(scope="session", autouse=True)
def is_headless(request, get_config):

    headless_option = request.config.getoption("--headless", default=None)
    if headless_option:
        log_allure(
            f"Select headless execution by terminal: HEADLESS {headless_option.upper()}"
        )
        return headless_option

    log_allure(
        f'Select headless execution by config file -> {CONFIG_YAML_PATH}: HEADLESS {get_config["HEADLESS"]}'
    )
    return get_config["HEADLESS"]


@pytest.fixture(scope="session", autouse=True)
def set_environment_variables(env, is_pipeline, is_headless):
    """
    Loads environment variables into the project before running tests.
    """
    dot_env = SetDotEnv()
    dot_env.set_project_environment_variables(is_pipeline, env, is_headless)


@pytest.fixture(scope="function")
def web_page(browser: Browser, get_config) -> Generator[Page, None, None]:
    """Creates a new page with web configuration"""
    web_config = get_config["WEB_CONFIG"]
    timeout = web_config.get("TIMEOUT")

    # Cria o contexto com todas as configurações do WEB_CONFIG
    context = browser.new_context(**web_config)
    page = context.new_page()
    page.set_default_timeout(timeout)
    yield page
    context.close()


@pytest.fixture(scope="function")
def mobile_page(browser: Browser, get_config) -> Generator[Page, None, None]:
    """Creates a new page with mobile configuration"""
    mobile_config = get_config["MOBILE_CONFIG"]
    timeout = mobile_config.get("TIMEOUT")

    context = browser.new_context(**mobile_config)
    page = context.new_page()
    page.set_default_timeout(timeout)
    yield page
    context.close()


@pytest.fixture(scope="module")
def db_manager(get_config, env):
    """Fixture that provides a database connection for tests."""
    common = Common(env, get_config)
    db = None

    try:
        db = common.get_db_manager()
        if not db or not db.connection.is_connected():
            pytest.skip("Database connection could not be established")

        yield db

    except Exception as e:
        pytest.fail(f"Database setup failed: {str(e)}")

    finally:
        if db and isinstance(db, DatabaseManager):
            try:
                db.close_connection()
            except Exception as e:
                print(f"Warning: Error closing connection: {e}")


def create_page_fixture(page_class):
    """Função auxiliar para criar fixtures de pages"""

    @pytest.fixture
    def web_fixture(web_page):
        return page_class(web_page)

    @pytest.fixture
    def mobile_fixture(mobile_page):
        return page_class(mobile_page)

    return web_fixture, mobile_fixture


# Criar fixtures para cada page
web_home_page, mobile_home_page = create_page_fixture(HomePage)
web_login_page, mobile_login_page = create_page_fixture(LoginPage)
