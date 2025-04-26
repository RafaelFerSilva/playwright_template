from typing import Optional

import allure

from utils.DatabaseManager import DatabaseManager
from utils.decorators import capture_on_failure


class UserDatabaseHandler:

    def __init__(self, env, db_manager: DatabaseManager):
        self.db_manager = db_manager
        self.env = env

    @capture_on_failure
    @allure.step("Fetching all users from the database")
    def get_users(self) -> Optional[dict]:
        """Fetches all users from the database."""
        return self.db_manager.execute_script("resources/sql/users.sql")
