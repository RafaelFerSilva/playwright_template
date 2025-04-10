import allure
from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @allure.step("Navigate to Page")
    def navigate_to(self, url: str):
        self.page.goto(url)

    @allure.step("Get Element")
    def get_element(self, selector: str):
        return self.page.locator(selector)
    
    @allure.step("Get Page Title")
    def get_page_title(self) -> str:
        return self.page.title()

    @allure.step("Click Element")
    def click_element(self, selector: str):
        self.get_element(selector).click()
    
    @allure.step("Fill Text")
    def fill_text(self, selector: str, text: str):
        self.get_element(selector).fill(text)

    @allure.step("Get Element")
    def get_text(self, selector: str) -> str:
        return self.get_element(selector).text_content()

    @allure.step("Is Visible")
    def is_visible(self, selector: str) -> bool:
        return self.get_element(selector).is_visible()

    @allure.step("Wait For Element")
    def wait_for_element(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, timeout=timeout)
