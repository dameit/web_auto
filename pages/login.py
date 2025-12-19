from pages.base import base_page
from common.config_read import ConfigRead

class login_page(base_page):
    def __init__(self, ip, username, password):
        super().__init__()
        self.ip, self.username, self.password = ip, username, password
    
    def open_browser(self):
        self.webdriver.get(f"http://{self.ip}")

    def input_username(self):
        username_by_locator = self.config.get("login_page", "username").split(', ')
        element = self.find_element(*username_by_locator)
        self.input_text(element=element, text=self.username)

    def input_password(self):
        password_by_locator = self.config.get("login_page", "password").split(', ')
        element = self.find_element(*password_by_locator)
        self.input_text(element=element, text=self.password)

    def login_click(self):
        login_button_by_locator = self.config.get("login_page", "login_button").split(', ')
        element = self.find_element(*login_button_by_locator)
        self.click_element(element=element)

    def handle_alert(self):
        from selenium.webdriver.support.ui import WebDriverWait
        from selenium.webdriver.support import expected_conditions as EC
        WebDriverWait(self.webdriver, 5).until(EC.alert_is_present())
        alert = self.webdriver.switch_to.alert
        alert.accept()

    def login_auto(self):
        self.open_browser()
        self.input_username()
        self.input_password()
        self.login_click()
        self.handle_alert()