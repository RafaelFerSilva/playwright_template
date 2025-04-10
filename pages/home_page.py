import allure
from .base_page import BasePage
from playwright.sync_api import Page

class HomePage(BasePage):
    def __init__(self, page: Page, base_url):
        super().__init__(page)
        self.page = page
        self.base_url = base_url
        self.page_title = "DEMOQA"

    @allure.step("Open Home Page")
    def navigate(self):
        self.navigate_to(self.base_url)
    
    @allure.step("Validate Home Page Title")
    def has_title(self):
        self.check_if_page_has_title(self.page_title)
