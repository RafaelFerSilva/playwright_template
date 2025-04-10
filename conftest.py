import pytest
import allure
import os
from playwright.sync_api import Page
from typing import Generator
from utils.ReadFile import ReadFile
from utils.logger import log_allure
from utils.SetDotEnv import SetDotEnv

CONFIG_YAML_PATH = './config.yaml'

def pytest_addoption(parser):
    parser.addoption("--env", action="store", help="Execution environment: rc, uat")
    parser.addoption("--pipeline", action="store", help="Run tests in pipeline: true, false")

@pytest.fixture(scope="function")
def page(browser) -> Generator[Page, None, None]:
    page = browser.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield page
    page.close()

@pytest.fixture(scope="session", autouse=True)
def env(request):

    env_option = request.config.getoption("--env", default=None)
    if env_option:
        log_allure(
            f'Select environment by terminal: ENVIRONMENT {env_option.upper()}')
        return env_option

    read_file = ReadFile()
    config = read_file.load_yaml_file(CONFIG_YAML_PATH)
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

@pytest.fixture(scope="session", autouse=True)
def base_url(request, set_environment_variables):
    """
    Returns the base URL from environment variables with error handling.
    """
    try:
        base_url = request.config.getoption("--base-url")
        if base_url:
            return base_url

        if 'URL' not in os.environ:
            raise KeyError(
                "URL environment variable is not set. "
                "Please check if set_environment_variables is working correctly "
                "or provide --base-url via command line."
            )

        return os.environ['URL']
    except Exception as e:
        pytest.fail(f"Failed to get base URL: {str(e)}")
