import os
import shutil
import pytest
from pages.login_page import LoginPage
from playwright.sync_api import Page
from utils.logs.logger import Logger


@pytest.fixture()
def login(page: Page, request):
    # Open and return Login page and prepare it to logging process

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
    # Add START and END marks before each test to separate them.

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


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    # Before each test run clear "allure-results" and "test-results" folders
    
    allure_dir = os.path.join(os.getcwd(), "allure-results")
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
        os.makedirs(allure_dir)

    img_vid_dir = os.path.join(os.getcwd(), "test-results")
    if os.path.exists(img_vid_dir):
        shutil.rmtree(img_vid_dir)
        os.makedirs(img_vid_dir)