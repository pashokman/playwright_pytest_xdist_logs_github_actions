from pages.herokuapp_login_page import HerokuLoginPage
from utils.logs.logger_with_context import get_logger_with_context

"""
Each test should have only one assertion. These tests contain many assertions just for education purposes.
"""


def test_first_login(next_authorization) -> None:

    assert next_authorization.is_first_message_present()
    assert next_authorization.is_first_message_has_text("You logged into a secure area!")
    assert next_authorization.is_second_message_has_text(
        "Welcome to the Secure Area. When you are done click logout below."
    )
    assert next_authorization.is_logout_btn_present()


def test_reload_page_after_login(set_up_tear_down, request) -> None:
    page = set_up_tear_down
    page.reload()
    page.wait_for_load_state("networkidle")

    log = get_logger_with_context(request=request, log_name="Heroku login page")
    login_page = HerokuLoginPage(page, log)

    assert not login_page.is_first_message_present()
    assert login_page.is_second_message_has_text("Welcome to the Secure Area. When you are done click logout below.")
    assert login_page.is_logout_btn_present()


def test_logout(set_up_tear_down, request):
    page = set_up_tear_down

    log = get_logger_with_context(request=request, log_name="Heroku login page")
    login_page = HerokuLoginPage(page, log)
    login_page.logout()

    assert login_page.is_first_message_has_text("You logged out of the secure area!")
