from typing import Dict, Generator

import pytest
from playwright.sync_api import Browser, Page

from pages.home_page import HomePage
from pages.login_page import LoginPage
from utils.Common import Common
from utils.DatabaseManager import DatabaseManager
from utils.logger import log_allure
from utils.ReadFile import ReadFile
from utils.SetDotEnv import SetDotEnv
from utils.url_helper import set_pytest_config

CONFIG_YAML_PATH = "./config.yaml"


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
def set_environment_variables(request, env):
    """
    Loads environment variables into the project before running tests.
    """
    dot_env = SetDotEnv()
    environment = request.config.getoption("--env", default=None)
    pipeline = request.config.getoption("--pipeline", default=False)

    if environment:
        dot_env.set_project_environment_variables(pipeline, environment)
    else:
        dot_env.set_project_environment_variables(pipeline, env)


@pytest.fixture(scope="function")
def web_page(browser: Browser, get_config) -> Generator[Page, None, None]:
    """Creates a new page with web configuration"""
    web_config = get_config["WEB_CONFIG"]

    # Cria o contexto com todas as configurações do WEB_CONFIG
    context = browser.new_context(**web_config)
    page = context.new_page()
    yield page
    context.close()


@pytest.fixture(scope="function")
def mobile_page(
    browser: Browser, get_config, playwright
) -> Generator[Page, None, None]:
    """Creates a new page with mobile configuration"""
    mobile_config = get_config["MOBILE_CONFIG"]
    context = browser.new_context(**mobile_config)
    page = context.new_page()
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
