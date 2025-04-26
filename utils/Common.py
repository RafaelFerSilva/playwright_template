import os

import allure

from .DatabaseManager import DatabaseManager

CONFIG_YAML_PATH = "./config.yaml"


class Common:
    """
    The Common class provides methods to handle URLs, manage database connections,
    and load translations from configured files.

    Args:
        environment (str): The execution environment (e.g., 'uat', 'rc', 'prod').
    """

    def __init__(self, environment, get_config):
        """
        Initializes the Common class with the provided environment and loads the configuration from a YAML file.

        Args:
            environment (str): The execution environment.
        """
        self.config = get_config
        self.environment = environment

    @allure.step("Get DB Manager")
    def get_db_manager(self) -> DatabaseManager:
        """
        Returns an instance of the database manager connected using environment variables.

        Returns:
            DatabaseManager: The connected database manager object.

        Raises:
            RuntimeError: If there is an error connecting to the database.
        """
        db_config = {
            "DB_NAME": os.getenv("DB_NAME"),
            "DB_USER": os.getenv("DB_USER"),
            "DB_PASSWORD": os.getenv("DB_PASSWORD"),
            "DB_HOST": os.getenv("DB_HOST"),
            "DB_PORT": int(os.getenv("DB_PORT", "3306")),  # Conversão explícita
        }

        # Verificação de configuração mínima
        if not all(db_config.values()):
            missing = [k for k, v in db_config.items() if not v]
            raise RuntimeError(f"Missing database configuration: {', '.join(missing)}")

        db = DatabaseManager(db_config, self.config)
        db.connect()
        return db
