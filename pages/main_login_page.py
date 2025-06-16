from typing import Any


class Login:
    """
    Base page class for login functionality.
    """

    URL: str | None = None

    USERNAME_FIELD_LOC: str | None = None
    USERPWD_FIELD_LOC: str | None = None
    LOGIN_BTN_LOC: str | None = None

    def __init__(self, page: Any, logger: Any):
        """
        :param page: Playwright page object
        :param logger: Logger instance
        """
        self.page = page
        self.logger = logger

    def fill_usrname_field(self, usrname: str):
        try:
            self.page.locator(self.USERNAME_FIELD_LOC).fill(usrname)
            self.logger.info(f"Useraname field filled with '{usrname}'")
        except Exception as e:
            self.logger.error(f"{str(e)}")
            raise

    def fill_usrpwd_field(self, pwd: str):
        try:
            self.page.locator(self.USERPWD_FIELD_LOC).fill(pwd)
            self.logger.info(f"Password field filled with '{pwd}'")
        except Exception as e:
            self.logger.error(f"{str(e)}")
            raise

    def click_login_button(self):
        try:
            self.page.locator(self.LOGIN_BTN_LOC).click()
            self.logger.info(f"Click on login btn successful.")
        except Exception as e:
            self.logger.error(f"{str(e)}")
            raise

    def goto_base_url(self):
        if not self.URL:
            raise ValueError("BASE_URL environment variable is not set!")
        try:
            self.page.goto(self.URL)
            self.logger.info(f"BASE_URL - opened!")
        except Exception as e:
            self.logger.error(f"{str(e)}")
            raise

    def fill_login_credentials(self, name: str, pwd: str):
        self.fill_usrname_field(name)
        self.fill_usrpwd_field(pwd)

    def login(self, name: str, pwd: str):
        self.fill_login_credentials(name, pwd)
        self.click_login_button()
