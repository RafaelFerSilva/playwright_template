"""
Screenshot Utility for Error Capturing and Reporting

This module provides a function to capture screenshots during test execution and attach them to Allure reports.

Functions:
    save_screenshot(self, func_name, type='PNG', folder="screenshots"):
        Captures a screenshot of the current page, saves it to a specified folder, and logs it in Allure.

Args:
    self: Object with a `page` attribute that supports a `screenshot` method.
    func_name (str): The name of the function triggering the screenshot.
    type (str): The type of attachment for Allure (default: 'PNG').
    folder (str): The directory where screenshots will be saved (default: "screenshots").

Behavior:
    - Creates the screenshots directory if it does not exist.
    - Appends a timestamp to the screenshot file name for uniqueness.
    - Attaches the screenshot as a binary file to Allure reports.
"""

import os
import allure
from datetime import datetime
from .logger import log_allure


@allure.step("Save Screenshot")
def save_screenshot(self, func_name, type='PNG', folder="screenshots"):
    """
    Captures a screenshot of the current page, saves it, and attaches it to an Allure report.

    Args:
        self: Object containing the `page` attribute for screenshot capture.
        func_name (str): Name of the function where the screenshot is triggered.
        type (str): Attachment type for Allure (default is 'PNG').
        folder (str): Directory to save the screenshots (default is 'screenshots').

    Process:
        - Generates a file name with a timestamp.
        - Ensures the directory for saving screenshots exists.
        - Saves the screenshot in the specified folder.
        - Attaches the screenshot to Allure with the specified type.
    """
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    screenshot_path = f"{folder}/{func_name}_{timestamp}.png"

    # Ensure the folder exists
    os.makedirs(folder, exist_ok=True)

    # Capture and save the screenshot
    self.page.screenshot(path=screenshot_path)

    # Attach the screenshot to the Allure report
    with open(screenshot_path, 'rb') as f:
        log_allure(
            message=f.read(),
            name=f"{func_name}_screenshot_{timestamp}",
            type=type
        )
