import pytest

from database.users import UserDatabaseHandler


@pytest.fixture(scope="function")
def database_users(env, db_manager) -> UserDatabaseHandler:
    return UserDatabaseHandler(env, db_manager)
