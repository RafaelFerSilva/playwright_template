import pytest
from playwright.sync_api import Page, expect
from typing import Generator

@pytest.fixture(scope="function")
def page(browser) -> Generator[Page, None, None]:
    page = browser.new_page()
    page.set_viewport_size({"width": 1920, "height": 1080})
    yield page
    page.close()

@pytest.fixture(scope="session")
def browser_context_args(browser_context_args):
    return {
        **browser_context_args,
        "viewport": {"width": 1920, "height": 1080},
        "record_video_dir": "videos/"
    }