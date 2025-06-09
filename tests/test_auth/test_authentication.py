from playwright.sync_api import expect


def test_first_login(next_authorization) -> None:
    context = next_authorization
    page = context.pages[0]

    expect(page.locator("#flash")).to_be_attached()
    expect(page.locator("#flash")).to_contain_text("You logged into a secure area!")
    expect(page.locator("h4")).to_contain_text("Welcome to the Secure Area. When you are done click logout below.")
    expect(page.locator("#content")).to_contain_text("Logout")


def test_reload_page_after_login(set_up_tear_down) -> None:
    page = set_up_tear_down
    page.reload()
    page.wait_for_load_state("networkidle")

    expect(page.locator("#flash")).not_to_be_attached()
    expect(page.locator("h4")).to_contain_text("Welcome to the Secure Area. When you are done click logout below.")
    expect(page.locator("#content")).to_contain_text("Logout")


def test_logout(set_up_tear_down):
    page = set_up_tear_down
    page.locator('//a[@href="/logout"]').click()

    expect(page.locator("#flash")).to_contain_text("You logged out of the secure area!")
