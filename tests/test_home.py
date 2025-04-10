import pytest
import allure
from pages.home_page import HomePage

class TestHome:
    @pytest.fixture
    def home_page(self, page) -> HomePage:
        return HomePage(page)

    @allure.title('Check Page Title')
    def test_check_page_title(self, home_page: HomePage):
        home_page.navigate()
        home_page.has_title()
