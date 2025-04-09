from playwright.sync_api import Page

class BasePage:
    def __init__(self, page: Page):
        self.page = page

    def navigate_to(self, url: str):
        self.page.goto(url)

    def get_element(self, selector: str):
        return self.page.locator(selector)
    
    def get_page_title(self) -> str:
        return self.page.title()

    def click_element(self, selector: str):
        self.get_element(selector).click()

    def fill_text(self, selector: str, text: str):
        self.get_element(selector).fill(text)

    def get_text(self, selector: str) -> str:
        return self.get_element(selector).text_content()

    def is_visible(self, selector: str) -> bool:
        return self.get_element(selector).is_visible()

    def wait_for_element(self, selector: str, timeout: int = 5000):
        self.page.wait_for_selector(selector, timeout=timeout)
