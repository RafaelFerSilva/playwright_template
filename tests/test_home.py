import pytest
from page_objects.home_page import HomePage

class TestLogin:
    @pytest.fixture
    def home_page(self, page):
        return HomePage(page)

    def test_check_page_title(self, home_page):
        home_page.navigate_to("https://demoqa.com/")
        title = home_page.get_page_title()
        assert title == "DEMOQA"

