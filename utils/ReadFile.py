import os

import allure
import yaml

from .logger import log_allure


class ReadFile:
    def __init__(self):
        pass

    @allure.step("Load config from yaml")
    def load_yaml_file(self, config_file: str, override: dict = None):
        """
        Loads a YAML file and allows overriding with values passed per parameter.

        :param config_file: YAML file path
        :param override: Dictionary with values to override
        :return: Dictionary with final settings
        """
        if not os.path.exists(config_file):
            raise FileNotFoundError(f"Config file not found: {config_file}")

        try:
            with open(config_file, "r") as file:
                config = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error reading YAML file: {e}")

        if override:
            config.update(override)

        log_allure(f"File content: {config}")

        return config
