import allure
from playwright.sync_api import Page, expect

from utils.decorators import capture_on_failure


class BasePage:
    def __init__(self, page: Page):
        self.page = page

    @capture_on_failure
    @allure.step("Navigate to Page")
    def navigate_to(self, url: str):
        self.page.goto(url)

    @capture_on_failure
    @allure.step("Get Element")
    def get_element(self, selector: str):
        return self.page.locator(selector)

    @capture_on_failure
    @allure.step("Get Page Title")
    def get_page_title(self) -> str:
        return self.page.title()

    @capture_on_failure
    @allure.step("Click Element")
    def click_element(self, selector: str):
        self.get_element(selector).click()

    @capture_on_failure
    @allure.step("Fill Text")
    def fill_text(self, selector: str, text: str):
        self.get_element(selector).fill(text)

    @capture_on_failure
    @allure.step("Get Element")
    def get_text(self, selector: str) -> str:
        return self.get_element(selector).text_content()

    @capture_on_failure
    @allure.step("Is Visible")
    def is_visible(self, selector: str) -> bool:
        return self.get_element(selector).is_visible()

    @capture_on_failure
    @allure.step("Wait For Element")
    def wait_for_element(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, timeout=timeout)

    @capture_on_failure
    @allure.step("Validate page title")
    def check_if_page_has_title(self, title):
        expect(self.page).to_have_title(title)
