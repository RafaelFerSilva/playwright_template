import pytest
from playwright.sync_api import Page
from typing import Generator

@pytest.fixture(scope="function")
def page(browser) -> Generator[Page, None, None]:
    page = browser.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield page
    page.close()
