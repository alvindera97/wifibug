import os
import sys
from typing import Dict, Callable, Optional, NoReturn

from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome

USAGE_TEXT: str = "USAGE: python main.py [headless/visual] [username password]\n"
EXECUTE: Dict[Optional[int], Callable] = {
    2: lambda: main(
        headless=True if sys.argv[1] == "headless" else False),
    4: lambda: main(
        headless=True if sys.argv[1] == "headless" else False,
        username=sys.argv[2],
        password=sys.argv[3]),
    None: lambda: print(USAGE_TEXT)
}


def raise_no_username_password_set():
    print(USAGE_TEXT)
    quit(0)


def main(
        headless: bool = False,
        username: str = None,
        password: str = None) -> NoReturn:
    """
    Persistently try to login to UNIBEN wifi given username and password.

    If username and password is given,
    the given username and password combinations are used login,
    if given username and password combinations are incorrect however,
     main() fails instantly displaying the error

    If username and password aren't given,
    environment variables storing "UNIBEN_WIFI_USERNAME' and
    'UNIBEN_WIFI_PASSWORD' are used as credentials.
    If no environment variable for 'UNIBEN_WIFI_USERNAME'
    and [or] 'UNIBEN_WIFI_PASSWORD' exist,
    main() raises NoUsernamePasswordSetError

    It's following operation is the same as if username
    and password were originally given.
    """

    if not (username and password):
        username = os.getenv('UNIBEN_WIFI_USERNAME', raise_no_username_password_set())
        password = os.getenv('UNIBEN_WIFI_PASSWORD', raise_no_username_password_set())

    if headless:
        options = Options()
        options.headless = True
        browser = Chrome(chrome_options=options)
    else:
        browser = Chrome()


if __name__ == "__main__":
    EXECUTE[len(sys.argv) if len(sys.argv) in EXECUTE else None]()
