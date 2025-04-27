import allure

from pages.home_page import HomePage


class TestHome:
    @allure.title("Check Page Title - Web")
    def test_check_page_title_web(self, web_home_page: HomePage):
        web_home_page.navigate()
        web_home_page.has_title()

    @allure.title("Check Page Title - Mobile")
    def test_check_page_title_mobile(self, mobile_home_page: HomePage):
        mobile_home_page.navigate()
        mobile_home_page.has_title()
