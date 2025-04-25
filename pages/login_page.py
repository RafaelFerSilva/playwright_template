import allure
from playwright.sync_api import Page

from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.url = "https://demoqa.com/login"
        self.page_title = "DEMOQA"

    @allure.step("Open Login Page")
    def navigate(self):
        self.navigate_to(self.url)
    
    @allure.step("Validate Login Page Title")
    def has_title(self):
        self.check_if_page_has_title(self.page_title)
