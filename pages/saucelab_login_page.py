import os
from playwright.sync_api import expect
from pages.main_login_page import Login


class SauceLoginPage(Login):

    URL = os.environ.get("SOUCELAB_BASE_URL")

    USERNAME_FIELD_LOC = '[data-test="username"]'
    USERPWD_FIELD_LOC = '[data-test="password"]'
    LOGIN_BTN_LOC = '[data-test="login-button"]'

    BACKPACK_TEXT_LOC = '[data-test="item-4-title-link"] [data-test="inventory-item-name"]'

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

    def is_backpack_item_name_contain_text(self, text):
        try:
            expect(self.page.locator(self.BACKPACK_TEXT_LOC)).to_contain_text(text)
            self.logger.info(f"Backpack item name contains text '{text}'")
        except Exception as e:
            self.logger.error(f"{str(e)}")
            raise
