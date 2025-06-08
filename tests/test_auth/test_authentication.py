def test_first_login(next_authorization) -> None:
    context = next_authorization
    page = context.pages[0]
    assert page.locator("#flash").count() == 1
    assert "You logged into a secure area!" in page.locator("#flash").text_content()
    assert "Welcome to the Secure Area. When you are done click logout below." in page.locator("h4").text_content()
    assert "Logout" in page.locator("#content").text_content()


def test_reload_page_after_login(set_up_tear_down) -> None:
    page = set_up_tear_down
    page.reload()
    page.wait_for_load_state("networkidle")

    assert page.locator("#flash").count() == 0
    assert "Welcome to the Secure Area. When you are done click logout below." in page.locator("h4").text_content()
    assert "Logout" in page.locator("#content").text_content()


def test_logout(set_up_tear_down):
    page = set_up_tear_down
    page.locator('//a[@href="/logout"]').click()
    actual_text = page.locator("#flash").inner_text()

    assert "You logged out of the secure area!" in actual_text
