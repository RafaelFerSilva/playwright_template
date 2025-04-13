import allure
from pages.login_page import LoginPage

class TestLogin:
    @allure.title('Check Page Title - Login Web')
    def test_check_page_title_login_web(self, web_login_page: LoginPage):
        web_login_page.navigate()
        web_login_page.has_title()

    @allure.title('Check Page Title - Login Mobile')
    def test_check_page_title_login_mobile(self, mobile_login_page: LoginPage):
        mobile_login_page.navigate()
        mobile_login_page.has_title()
