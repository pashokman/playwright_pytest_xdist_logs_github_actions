import pytest
from utils.files_worker.get_credentials import get_credentials


CREDENTIALS = get_credentials("./data/login_credentials.csv")


@pytest.mark.smoke
@pytest.mark.parametrize(
    "credentials",
    CREDENTIALS,
    ids=[f"{cred['username'] or 'empty'}-{cred['password'] or 'empty'}" for cred in CREDENTIALS],
)
def test_item_names_text(login, credentials) -> None:
    login.login(credentials["username"], credentials["password"])
    login.is_backpack_item_name_contain_text("Sauce Labs Backpack")
