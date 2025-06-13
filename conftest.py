from pathlib import Path
import allure
import glob
import os
import pytest
import shutil

from dotenv import load_dotenv
from slugify import slugify
from pages.saucelab_login_page import SauceLoginPage
from playwright.sync_api import Page
from utils.logs.logger_with_context import get_logger_with_context
from utils.logs.logger import Logger


load_dotenv()


@pytest.fixture()
def login(page: Page, request):
    log = get_logger_with_context(request, log_name="Sauce login page")
    login_page = SauceLoginPage(page, logger=log)

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
    # Before each pytest run, clear "allure-results", "test-results", "report" folders and "automation.log" file
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

    log_file = os.path.join(os.getcwd(), "automation.log")
    if os.path.exists(log_file):
        with open(log_file, "w"):
            pass


@pytest.hookimpl(tryfirst=True, hookwrapper=True)
def pytest_runtest_makereport(item, call):
    # Execute all other hooks to obtain the report object
    pytest_html = item.config.pluginmanager.getplugin("html")
    outcome = yield
    report = outcome.get_result()

    # Only add attachments for actual failed test calls, not setup/teardown
    if report.when == "call" and report.failed:
        # Attach screenshots to allure-report
        screenshots = glob.glob("test-results/**/*.png", recursive=True)
        for screenshot in screenshots:
            with open(screenshot, "rb") as f:
                allure.attach(f.read(), name=os.path.basename(screenshot), attachment_type=allure.attachment_type.PNG)
        # Attach videos to allure-report
        videos = glob.glob("test-results/**/*.webm", recursive=True)
        for video in videos:
            with open(video, "rb") as f:
                allure.attach(f.read(), name=os.path.basename(video), attachment_type=allure.attachment_type.WEBM)

        # Pytest-html screenshot attachment
        extras = getattr(report, "extras", [])
        if report.failed and "page" in item.funcargs and pytest_html:
            page = item.funcargs["page"]
            screenshot_dir = Path("test-results")
            screenshot_dir.mkdir(exist_ok=True)
            screen_file = screenshot_dir / f"{slugify(item.nodeid)}.png"
            page.screenshot(path=str(screen_file))
            rel_path = os.path.relpath(screen_file, "report")
            extras.append(pytest_html.extras.image(rel_path))
        report.extras = extras
