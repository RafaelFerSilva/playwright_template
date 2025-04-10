import pytest
import allure
from page_objects.home_page import HomePage
from utils.asserts import BaseAsserts

class TestHome:
    @pytest.fixture
    def home_page(self, page) -> HomePage:
        return HomePage(page)

    @allure.title('Check Page Title')
    def test_check_page_title(self, home_page: HomePage):
        home_page.navigate_to("https://demoqa.com/")
        title = home_page.get_page_title()
        assert title == "DEMOQA"
    
    @allure.title('Check Page Error')
    def test_check_page_title2(self, home_page: HomePage):
        home_page.navigate_to("https://demoqa.com/")
        title = home_page.get_page_title()
        BaseAsserts.assert_string_value(self, "DEMOQ", title)

