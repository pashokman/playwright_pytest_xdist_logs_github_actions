import os
from pages.main_login_page import Login


class HerokuLoginPage(Login):

    URL = os.environ.get("HEROKUAPP_BASE_URL")

    USERNAME_FIELD_LOC = "#username"
    USERPWD_FIELD_LOC = "#password"
    LOGIN_BTN_LOC = "//button"

    FIRST_MESSAGE_LOC = "#flash"
    SECOND_MESSAGE_LOC = "h4"
    LOGOUT_BTN_TEXT_LOC = "#content"
    LOGOUT_BTN_LOC = '//a[@href="/logout"]'

    def __init__(self, page, logger):
        self.page = page
        self.logger = logger

    def goto_base_url(self):
        if not self.URL:
            raise ValueError("BASE_URL environment variable is not set!")
        try:
            self.page.goto(self.URL + "/login")
            self.logger.info(f"BASE_URL - opened!")
        except Exception as e:
            self.logger.error(f"{str(e)}")
            raise

    def is_first_message_present(self):
        return self.page.locator(self.FIRST_MESSAGE_LOC).count() == 1

    def get_first_message_text(self):
        return self.page.locator(self.FIRST_MESSAGE_LOC).inner_text()

    def is_first_message_has_text(self, text):
        return text in self.get_first_message_text()

    def get_second_message_text(self):
        return self.page.locator(self.SECOND_MESSAGE_LOC).inner_text()

    def is_second_message_has_text(self, text):
        return text in self.get_second_message_text()

    def is_logout_btn_present(self):
        return self.page.locator(self.LOGOUT_BTN_TEXT_LOC).count() == 1

    def logout(self):
        try:
            self.page.locator(self.LOGOUT_BTN_LOC).click()
            self.logger.info(f"Logged out successfull!")
        except Exception as e:
            self.logger.error(f"{str(e)}")
            raise
