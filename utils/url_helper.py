import os
from typing import Optional

import allure
import pytest
from pytest import Config

from utils.logger import log_allure

_config: Optional[Config] = None


def set_pytest_config(config: Config):
    """Configura o config para uso no get_base_url"""
    global _config
    _config = config


@allure.step("Get Base URL")
def get_base_url() -> str:
    """
    Returns the base URL in the following order:
    1. Environment variable 'URL'
    2. pytest.ini configuration 'base_url'
    3. Raises error if neither is found
    """
    try:
        # 1. Tenta obter do ambiente
        if "URL" in os.environ:
            log_allure(f"Set base_url by environment: {os.environ['URL']}")
            return os.environ["URL"]

        # 2. Tenta obter do pytest.ini
        if _config and _config.inicfg.get("base_url"):
            log_allure(f"Set base_url by pytestini: {_config.inicfg['base_url']}")
            return _config.inicfg["base_url"]

        # 3. Se não encontrar em nenhum lugar, lança exceção
        raise KeyError(
            "Base URL not found. Please set either:\n"
            "1. Environment variable 'URL'\n"
            "2. base_url in pytest.ini"
        )
    except Exception as e:
        pytest.fail(f"Failed to get base URL: {str(e)}")
