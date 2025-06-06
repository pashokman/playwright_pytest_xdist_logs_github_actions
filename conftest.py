import allure
import glob
import os
import pytest
import shutil

from dotenv import load_dotenv
from pages.login_page import LoginPage
from playwright.sync_api import Page
from utils.logs.logger import Logger


load_dotenv()


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
    login_page.goto_base_url()
    return login_page


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


@pytest.fixture(scope="function", autouse=True)
def set_viewport_size(page):
    width = int(os.environ.get("VIEWPORT_WIDTH", 1920))
    height = int(os.environ.get("VIEWPORT_HEIGHT", 945))
    page.set_viewport_size({"width": width, "height": height})


@pytest.hookimpl(tryfirst=True)
def pytest_sessionstart(session):
    # Before each pytest run, clear "allure-results" and "test-results" folders
    allure_dir = os.path.join(os.getcwd(), "allure-results")
    if os.path.exists(allure_dir):
        shutil.rmtree(allure_dir)
        os.makedirs(allure_dir)

    img_vid_trace_dir = os.path.join(os.getcwd(), "test-results")
    if os.path.exists(img_vid_trace_dir):
        shutil.rmtree(img_vid_trace_dir)
        os.makedirs(img_vid_trace_dir)

    html_report = os.path.join(os.getcwd(), "report")
    if os.path.exists(html_report):
        shutil.rmtree(html_report)
        os.makedirs(html_report)


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    outcome = yield
    rep = outcome.get_result()

    # Only add attachments for actual test calls, not setup/teardown
    if rep.when == "call" and rep.failed:
        # Attach screenshots
        screenshots = glob.glob("test-results/**/*.png", recursive=True)
        for screenshot in screenshots:
            with open(screenshot, "rb") as f:
                allure.attach(f.read(), name=os.path.basename(screenshot), attachment_type=allure.attachment_type.PNG)
        # Attach videos
        videos = glob.glob("test-results/**/*.webm", recursive=True)
        for video in videos:
            with open(video, "rb") as f:
                allure.attach(f.read(), name=os.path.basename(video), attachment_type=allure.attachment_type.WEBM)
