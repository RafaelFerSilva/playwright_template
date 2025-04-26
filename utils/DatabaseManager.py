import time
from pathlib import Path
from typing import Dict, List, Optional, Union

import allure
import mysql.connector

from utils.string_utils import replace_string

from .logger import log_allure, log_info


class DatabaseManager:
    """
    A comprehensive database manager for MySQL operations with connection handling,
    query execution, and environment-specific script management.

    Args:
        db_config (dict): Database configuration containing:
            - DB_HOST: Database server hostname
            - DB_PORT: Database server port
            - DB_NAME: Database name
            - DB_USER: Database username
            - DB_PASSWORD: Database password
        get_config (dict): Main configuration dictionary
    """

    def __init__(self, db_config: dict, get_config: dict):
        """
        Initializes the database manager with configuration settings.
        """
        self.config = get_config
        self.TIMEOUT = 60  # Maximum waiting time in seconds
        self.INTERVAL = 5  # Time between connection attempts
        self.ELAPSE_TIME = 0  # Tracks elapsed time
        self.DB_HOST = db_config["DB_HOST"]
        self.DB_PORT = db_config["DB_PORT"]
        self.DB_NAME = db_config["DB_NAME"]
        self.DB_USER = db_config["DB_USER"]
        self.DB_PASSWORD = db_config["DB_PASSWORD"]
        self.connection: Optional[mysql.connector.MySQLConnection] = None

    @allure.step("Connect To Database")
    def connect(self) -> None:
        """
        Establishes a connection to the MySQL database with retry logic.

        Raises:
            RuntimeError: If connection fails after timeout period
        """
        start_time = time.time()

        while (time.time() - start_time) < self.TIMEOUT:
            try:
                log_allure("Attempting to connect to MySQL database...")
                self.connection = mysql.connector.connect(
                    host=self.DB_HOST,
                    port=self.DB_PORT,
                    user=self.DB_USER,
                    password=self.DB_PASSWORD,
                    database=self.DB_NAME,
                    connect_timeout=5,
                )

                if self.connection.is_connected():
                    log_info("✅ Successfully connected to MySQL database!")
                    return

            except mysql.connector.Error as err:
                log_info(f"⚠️ Connection attempt failed: {err}")
                time.sleep(self.INTERVAL)
                continue

        raise RuntimeError(
            f"Failed to connect to database after {self.TIMEOUT} seconds"
        )

    @allure.step("Execute Query")
    def execute_script(self, script_path: Union[str, Path]) -> List[Dict]:
        """
        Executes a SQL script from file and returns results as dictionaries.

        Args:
            script_path: Path to the SQL script file

        Returns:
            List of dictionaries representing query results or message if empty

        Raises:
            RuntimeError: If execution fails or connection is not established
        """
        if not self.connection or not self.connection.is_connected():
            raise RuntimeError("Database connection is not established")

        try:
            with open(script_path, "r") as file:
                sql = file.read().strip()

            if not sql:
                raise ValueError("Script file is empty")

            with self.connection.cursor(dictionary=True) as cursor:
                log_info(f"Executing SQL: {sql}")
                cursor.execute(sql)

                if cursor.with_rows:
                    results = cursor.fetchall()
                    log_info(f"Query results: {results}")
                    return results

                return [
                    {
                        "message": "Query executed successfully",
                        "affected_rows": cursor.rowcount,
                    }
                ]

        except Exception as err:
            log_info(f"Error executing script: {err}")
            raise RuntimeError(f"Script execution failed: {err}")

    @allure.step("Replace Values And Execute Query")
    def replace_values_and_execute_script(
        self, script_path: Union[str, Path], values: List[str]
    ) -> List[Dict]:
        """
        Replaces placeholders in script and executes it.

        Args:
            script_path: Path to SQL script file
            values: List of values to replace placeholders

        Returns:
            List of dictionaries with query results
        """
        if not self.connection or not self.connection.is_connected():
            self.connect()

        try:
            with open(script_path, "r") as file:
                sql = file.read().strip()

            replaced_sql = replace_string(sql, "$$", values)
            return self.execute_sql(replaced_sql)

        except Exception as err:
            log_info(f"Error in value replacement: {err}")
            raise RuntimeError(f"Script execution failed: {err}")

    @allure.step("Execute Environment-Specific Query")
    def execute_script_by_environment(
        self, environment: str, script_name: str
    ) -> List[Dict]:
        """
        Executes a script from environment-specific folder.

        Args:
            environment: Target environment (e.g., 'uat', 'prod')
            script_name: Name of SQL script file

        Returns:
            List of dictionaries with query results
        """
        script_path = Path(
            f"{self.config['SQL_SCRIPTS_FOLDER']}/{environment}/{script_name}"
        )
        return self.execute_script(script_path)

    @allure.step("Replace Values in Environment-Specific Query")
    def replace_values_and_execute_script_by_environment(
        self, environment: str, script_name: str, values: List[str]
    ) -> List[Dict]:
        """
        Replaces values in environment-specific script and executes it.

        Args:
            environment: Target environment
            script_name: SQL script filename
            values: Values for placeholder replacement
        """
        script_path = Path(
            f"{self.config['SQL_SCRIPTS_FOLDER']}/{environment}/{script_name}"
        )
        return self.replace_values_and_execute_script(script_path, values)

    @allure.step("Disconnect From Database")
    def close_connection(self) -> None:
        """Closes the database connection if it exists and is open."""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            log_allure("Database connection closed")
            self.connection = None

    def __enter__(self):
        """Context manager entry point."""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit point."""
        if self.connection and self.connection.is_connected():
            self.close_connection()

    def execute_sql(self, sql: str) -> List[Dict]:
        """Internal method to execute raw SQL."""
        with self.connection.cursor(dictionary=True) as cursor:
            cursor.execute(sql)
            return cursor.fetchall() if cursor.with_rows else []
