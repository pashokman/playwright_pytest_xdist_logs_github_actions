import pytest
from pages.login_page import LoginPage
from playwright.sync_api import Page
from utils.logs.logger import Logger


@pytest.fixture()
def login(page: Page, request):
    browser_name = request.config.getoption("--browser")
    test_file = request.node.fspath
    test_name = request.node.name
    log_line_prefix = f"[{browser_name}]::{test_file}::{test_name}"

    logger_instance = Logger(log_name="Login page")
    logger_with_context = logger_instance.get_adapter(test_context=log_line_prefix)

    login_page = LoginPage(page, logger=logger_with_context)
    login_page.goto()
    return login_page


@pytest.fixture(scope="function", autouse=True)
def before_and_after_each_test(request):
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
