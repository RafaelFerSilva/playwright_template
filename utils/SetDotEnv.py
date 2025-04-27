import os

import allure
from dotenv import load_dotenv

from .logger import log_allure


class SetDotEnv:
    def __init__(self):
        pass

    @allure.step("Set Project Environment Variables")
    def set_project_environment_variables(
        self, pipeline: bool = False, environment: str = "rc", is_headless: bool = False
    ) -> dict:
        """
        Set Environment Project Variables

        This function configures environment variables for the current session. It supports two modes:

        1. Pipeline Mode (`pipeline=True`): Loads variables directly from the OS environment.
        2. File Environment Mode (`pipeline=False`): Loads variables from a `.env` file corresponding to the specified environment name.

        Args:
            pipeline (bool): Flag to determine if variables should be loaded from the OS environment (default: False).
            environment (str): The name of the `.env` file to load (default: 'rc').
            print_variables (bool): Flag to print loaded environment variables to the console (default: False).

        Returns:
            dict: Key-value pairs of the loaded environment variables.

        Raises:
            FileNotFoundError: If the specified `.env` file is not found.
            Exception: For other issues during variable loading.
        """
        try:
            if pipeline:
                variables = dict(os.environ)
                variables["HEADLESS"] = is_headless
                log_allure(f"Run tests on Pipeline: {pipeline}")
            else:
                env_file = f"{environment.lower()}.env"
                if not os.path.exists(env_file):
                    raise FileNotFoundError(f"Environment file '{env_file}' not found.")

                load_dotenv(env_file, override=True)
                log_allure(f"Loaded Environment file: {env_file}")
                variables = dict(os.environ)
                variables["HEADLESS"] = is_headless

            if variables:
                log_allure("ENVIRONMENTS VARIABLES SET WITH SUCCESS")
                return variables
            else:
                raise ValueError("No environment variables found.")

        except Exception as e:
            raise Exception(f"Error loading environment variables: {e}")
