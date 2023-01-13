import os
import sys
from typing import Dict, Callable, Optional, NoReturn

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.by import By

USAGE_TEXT: str = "USAGE: p" \
                  "ython main.py [headless/visual] [username password]\n"
LOGIN_URL = "http://hotspot.uniben.edu/login?dst=http://nmcheck.gnome.org/"

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


def raise_invalid_username_or_password():
    print(f'INVALID USERNAME OR PASSWORD!\n'
          f'Try again with correct credentials.'
          f'\n\n{USAGE_TEXT}')
    quit(0)


def raise_execution_failure(message) -> bool:
    print(f'{message}')
    return False


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
        username = os.getenv("UNIBEN_WIFI_USERNAME") if os.getenv(
            'UNIBEN_WIFI_USERNAME') else raise_no_username_password_set()
        password = os.getenv("UNIBEN_WIFI_PASSWORD") if os.getenv(
            'UNIBEN_WIFI_PASSWORD') else raise_no_username_password_set()

    if headless:
        options = Options()
        options.headless = True
        browser = Chrome(options=options)
    else:
        browser = Chrome()
    browser.implicitly_wait(5)

    verdict = False

    while not verdict:
        browser.get(LOGIN_URL)
        try:
            browser.find_element(By.XPATH,
                                 "/html/body/div/div/div/form/label[1]/input"
                                 ).send_keys(username)
            browser.find_element(By.XPATH,
                                 "/html/body/div/div/div/form/label[2]/input"
                                 ).send_keys(password)
            browser.find_element(By.XPATH,
                                 '/html/body/div/div/div/form/input[3]'
                                 ).click()
            message = browser.find_element(
                By.CSS_SELECTOR, "p.info.alert").text

            if message.startswith("invalid"):
                raise_invalid_username_or_password()
            elif message.startswith("no"):
                verdict = raise_execution_failure(message)
            else:
                verdict = False
        except NoSuchElementException:
            break
        except Exception as e:
            raise_execution_failure(e)
            quit(0)

    print("Logged In Successfully!")


if __name__ == "__main__":
    EXECUTE[len(sys.argv) if len(sys.argv) in EXECUTE else None]()
