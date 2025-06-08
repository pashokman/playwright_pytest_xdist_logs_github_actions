from playwright.sync_api import Playwright, expect
import pytest


@pytest.fixture(scope="session")
def next_authorization(playwright: Playwright):
    browser = playwright.chromium.launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    page.locator("//button").click()

    yield context


@pytest.fixture(scope="session")
def saved_context(playwright: Playwright, browser_name):
    browser = getattr(playwright, browser_name).launch(headless=False)
    context = browser.new_context()
    page = context.new_page()
    page.goto("https://the-internet.herokuapp.com/login")
    page.locator("#username").fill("tomsmith")
    page.locator("#password").fill("SuperSecretPassword!")
    page.locator("//button").click()
    # Wait for login to succeed
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
