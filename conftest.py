import pytest
import allure
import os
from playwright.sync_api import Page, Browser
from typing import Generator
from utils.ReadFile import ReadFile
from utils.logger import log_allure
from utils.SetDotEnv import SetDotEnv
from pages.home_page import HomePage
from pages.login_page import LoginPage

CONFIG_YAML_PATH = './config.yaml'

def get_config() -> dict:
    """Retorna as configurações do arquivo config.yaml"""
    read_file = ReadFile()
    return read_file.load_yaml_file(CONFIG_YAML_PATH)

def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Execution environment: rc, uat")
    parser.addoption("--pipeline", action="store", help="Run tests in pipeline: true, false")

@pytest.fixture(scope="session", autouse=True)
def env(request):

    env_option = request.config.getoption("--env", default=None)
    if env_option:
        log_allure(
            f'Select environment by terminal: ENVIRONMENT {env_option.upper()}')
        return env_option

    read_file = ReadFile()
    config = get_config()
    log_allure(
        f'Select environment by config file -> {CONFIG_YAML_PATH}: ENVIRONMENT {config["ENVIRONMENT"]}')
    return config["ENVIRONMENT"]

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
def web_page(browser: Browser) -> Generator[Page, None, None]:
    """Creates a new page with web configuration"""
    config = get_config()
    web_config = config.get("WEB_CONFIG", {})

    # Cria o contexto com todas as configurações do WEB_CONFIG
    context = browser.new_context(**web_config)
    page = context.new_page()
    yield page
    context.close()

@pytest.fixture(scope="function")
def mobile_page(browser: Browser, device_name: str = "Nexus 5") -> Generator[Page, None, None]:
    """Creates a new page with mobile configuration"""
    config = get_config()
    mobile_config = config.get("MOBILE_CONFIG", {})

    # Encontra a configuração específica do device
    device_config = next(
        (device for device in mobile_config.get("devices", [])
         if device["name"] == device_name),
        {}
    )

    # Remove o campo 'name' para não causar conflito
    if "name" in device_config:
        del device_config["name"]

    context = browser.new_context(**device_config)
    page = context.new_page()
    yield page
    context.close()

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
