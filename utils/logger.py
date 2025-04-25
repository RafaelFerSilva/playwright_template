"""
Logging Utility for Message Tracking and Reporting

This module provides utility functions for logging messages to both the console and Allure reports.

Functions:
    log_allure(message, name='Log info', type='TEXT'):
        Logs a message to Allure as an attachment with the specified type and name.

    log_error(message):
        Logs an error-level message to the console and Allure.

    log_info(message):
        Logs an info-level message to the console.

Behavior:
    - Uses Python's logging module for console output.
    - Logs messages in Allure for enhanced report tracking.

Logging Configuration:
    - Default logging level: INFO
    - Format: '[LEVEL] message'
    - Date format: 'dd-mm-yyyy HH:MM:SS'
"""

import logging

import allure

logging.getLogger("asyncio").setLevel(logging.WARNING)

# Configure logging
if not logging.getLogger().hasHandlers():
    logging.basicConfig(
        level=logging.INFO,
        format="[%(levelname)s] %(message)s",
        datefmt="%d-%m-%Y %H:%M:%S",
    )


@allure.step("Log - Allure")
def log_allure(message, name="Log info", type="TEXT"):
    """
    Logs a message to Allure as an attachment.

    Args:
        message (str): The message to be logged.
        name (str): The name of the attachment in the Allure report. Default is 'Log info'.
        type (str): The type of attachment (e.g., 'TEXT', 'HTML', etc.). Default is 'TEXT'.
    """
    allure.attach(message, name, attachment_type=allure.attachment_type[type])


def log_error(message):
    """
    Logs an error message.

    Args:
        message (str): The error message to log.
    """
    logging.error(message)
    log_allure(message, "Error Log")


def log_info(message):
    """
    Logs an informational message.

    Args:
        message (str): The info message to log.
    """
    logging.info(message)
