import allure
from .base_page import BasePage
from playwright.sync_api import Page, expect
from utils.decorators import capture_on_failure

class HomePage(BasePage):
    def __init__(self, page: Page):
        super().__init__(page)
        self.page = page
        self.url = "https://demoqa.com/"
        self.page_title = "DEMOQA"

    @allure.step("Open Home Page")
    def navigate(self):
        self.navigate_to(self.url)
    
    @allure.step("Validate Home Page Title")
    def has_title(self):
        self.check_if_page_has_title(self.page_title)
