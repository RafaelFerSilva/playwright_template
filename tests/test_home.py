import allure
from pages.home_page import HomePage
from pages.login_page import LoginPage

class TestHome:
    @allure.title('Check Page Title - Web')
    def test_check_page_title_web(self, web_home_page: HomePage):
        web_home_page.navigate()
        web_home_page.has_title()

    @allure.title('Check Page Title - Mobile')
    def test_check_page_title_mobile(self, mobile_home_page: HomePage):
        mobile_home_page.navigate()
        mobile_home_page.has_title()

    
    @allure.title('Check Page Title - Login Web')
    def test_check_page_title_login_web(self, web_login_page: LoginPage):
        web_login_page.navigate()
        web_login_page.has_title()

    @allure.title('Check Page Title - Login Mobile')
    def test_check_page_title_login_mobile(self, mobile_login_page: LoginPage):
        mobile_login_page.navigate()
        mobile_login_page.has_title()
