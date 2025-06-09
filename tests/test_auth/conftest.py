import pytest

from playwright.sync_api import Playwright, expect
from pages.herokuapp_login_page import HerokuLoginPage
from utils.logs.logger_with_context import get_logger_with_context
from utils.logs.logger import Logger
from dotenv import load_dotenv


load_dotenv()


@pytest.fixture()
def next_authorization(browser, request):
    context = browser.new_context()
    page = context.new_page()

    log = get_logger_with_context(request, log_name="Heroku login page")
    login_page = HerokuLoginPage(page, logger=log)

    login_page.goto_base_url()
    login_page.login("tomsmith", "SuperSecretPassword!")

    yield login_page


@pytest.fixture(scope="session")
def saved_context(playwright: Playwright, browser_name, request):
    browser = getattr(playwright, browser_name).launch()
    context = browser.new_context()
    page = context.new_page()

    log = get_logger_with_context(request=request, log_name="Heroku login page")
    login_page = HerokuLoginPage(page, logger=log)

    login_page.goto_base_url()
    login_page.login("tomsmith", "SuperSecretPassword!")

    expect(page).to_have_url("https://the-internet.herokuapp.com/secure")
    state_file = f"state_{browser_name}.json"
    context.storage_state(path=state_file)

    yield context

    context.close()
    browser.close()


@pytest.fixture()
def set_up_tear_down(saved_context, browser, browser_name):
    state_file = f"state_{browser_name}.json"
    context = browser.new_context(storage_state=state_file)
    page = context.new_page()
    page.goto("https://the-internet.herokuapp.com/secure")

    yield page

    context.close()


@pytest.fixture(scope="function", autouse=True)
def before_and_after_each_test(request):
    # Add START and END marks in logs before each test to separate them.
    test_file = request.node.fspath
    test_name = request.node.name
    browser_name = request.config.getoption("--browser")
    log_line_prefix = f"[{browser_name}]::{test_file}::{test_name}"

    logger_instance = Logger(log_name="Test log")
    logger_with_context = logger_instance.get_adapter(test_context=log_line_prefix)

    logger_with_context.info(f"[TEST START]")
    request.node._log_line_prefix = log_line_prefix

    yield

    logger_with_context.info(f"[TEST END]")
