from playwright.sync_api import expect


class LoginPage:

    URL = "https://www.saucedemo.com/"

    USERNAME_FIELD_LOC = '[data-test="username"]'
    USERPWD_FIELD_LOC = '[data-test="password"]'
    LOGIN_BTN_LOC = '[data-test="login-button"]'

    BACKPACK_TEXT_LOC = '[data-test="item-4-title-link"] [data-test="inventory-item-name"]'

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

    def goto(self):
        try:
            self.page.goto(self.URL)
            self.logger.info(f"URL - {self.URL} opened!")
        except Exception as e:
            self.logger.error(f"{str(e)}")

    def fill_usrname_field(self, usrname):
        try:
            self.page.locator(self.USERNAME_FIELD_LOC).fill(usrname)
            self.logger.info(f"Useraname field filled with '{usrname}'")
        except Exception as e:
            self.logger.error(f"{str(e)}")

    def fill_usrpwd_field(self, pwd):
        try:
            self.page.locator(self.USERPWD_FIELD_LOC).fill(pwd)
            self.logger.info(f"Password field filled with '{pwd}'")
        except Exception as e:
            self.logger.error(f"{str(e)}")

    def click_login_button(self):
        try:
            self.page.locator(self.LOGIN_BTN_LOC).click()
            self.logger.info(f"Click on login btn successful.")
        except Exception as e:
            self.logger.error(f"{str(e)}")

    def fill_login_credentials(self, name, pwd):
        self.fill_usrname_field(name)
        self.fill_usrpwd_field(pwd)

    def login(self, name, pwd):
        self.fill_login_credentials(name, pwd)
        self.click_login_button()

    def is_backpack_item_name_contain_text(self, text):
        try:
            expect(self.page.locator(self.BACKPACK_TEXT_LOC)).to_contain_text(text)
            self.logger.info(f"Backpack item name contains text '{text}'")
        except Exception as e:
            self.logger.error(f"{str(e)}")
