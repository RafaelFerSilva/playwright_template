import allure

from database.users import UserDatabaseHandler
from utils.DatabaseManager import DatabaseManager
from utils.logger import log_allure


class TestDataBase:

    @allure.title("Should be possible execute SQL Query string")
    def test_database_query_string(self, db_manager: DatabaseManager):
        result = db_manager.execute_sql("SELECT * FROM users LIMIT 1;")
        log_allure(result[0]["email"])

    @allure.title("Should be possible execute SQL Query file by file path")
    def test_database_query_file(self, db_manager: DatabaseManager):
        result = db_manager.execute_script("resources/sql/users.sql")
        print(result)

    @allure.title("Should be possible execute SQL Query file by environment and path")
    def test_database_query_environment_file(self, env, db_manager: DatabaseManager):
        result = db_manager.execute_script_by_environment(env, "users_env.sql")
        print(result)

    @allure.title(
        "Should be possible replace values execute SQL Query file by environment and path"
    )
    def test_database_query_replace_file(self, env, db_manager: DatabaseManager):
        result = db_manager.replace_values_and_execute_script_by_environment(
            env, "users_replace.sql", ["5"]
        )
        print(result)

    @allure.title("Should be possible to retrieve users from the database")
    def test_get_users(self, database_users: UserDatabaseHandler):
        users = database_users.get_users()
        print(users)
