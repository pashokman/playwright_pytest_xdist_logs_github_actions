import pytest


CREDENTIALS = [
    ("standard_user", "secret_sauce"),
    ("problem_user", "secret_sauce"),
    ("performance_glitch_user", "secret_sauce"),
    ("incorrect_login", "incorrect_pwd"),
]


@pytest.mark.smoke
@pytest.mark.parametrize(
    "username, password",
    CREDENTIALS,
    ids=[f"{cred[0] or 'empty'}-{cred[1] or 'empty'}" for cred in CREDENTIALS],
)
def test_item_names_text(login, username, password) -> None:
    login.login(username, password)
    login.is_backpack_item_name_contain_text("Sauce Labs Backpack")
