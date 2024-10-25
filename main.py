import os
import sys
from typing import Dict, Callable, Optional, Tuple, List

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.webdriver import WebDriver as Chrome
from selenium.webdriver.common.by import By

import utils
from . import USAGE_TEXT

LOGIN_URL = "http://hotspot.uniben.edu/login?dst=http://nmcheck.gnome.org/"

EXECUTE: Dict[Optional[int], Callable] = {
    None: lambda: print(USAGE_TEXT),
    2: lambda: main(sys.argv[1] == "headless"),

    # multiple username/password credentials,
    3: lambda: main(sys.argv[1] == "headless", username_password=sys.argv[2]),

    # single username/password credential
    4: lambda: main(sys.argv[1] == "headless", username_password=sys.argv[2] + sys.argv[3]),
}


def print_no_username_password_set_and_quit():
    """
    Print that username/password is incorrect, then quit application.
    """
    print(USAGE_TEXT)
    quit(0)


def print_invalid_username_or_password_and_quit():
    """
    Print that username/password invalid and quit application.
    """
    print(f'INVALID USERNAME OR PASSWORD!\n'
          f'Try again with correct credentials.'
          f'\n\n{USAGE_TEXT}')
    quit(0)


def print_execution_failure(message) -> bool:
    """
    Print execution failure message passed in the argument 'message'
    """
    print(f'{message}')
    return False


def main(
        headless: bool,
        username_password: str = None,
) -> None:
    """
    Tries to log in to UNIBEN Wi-Fi with provided or environment-stored credentials.

    ----------------- SINGLE USERNAME/PASSWORD -----------------------
    - If a username and password are provided, they will be used to log in.
    - If the credentials are incorrect, the program will fail and display an error.
    - If no credentials are provided, the program will use environment variables
      'UNIBEN_WIFI_USERNAME' and 'UNIBEN_WIFI_PASSWORD' as the credentials.

    ----------------- MULTIPLE USERNAME/PASSWORD COMBINATIONS -----------------------
    - Multiple username/password pairs can be provided, separated by semicolons (`;`).
      Example: "username1;;username2;password2"
    - If using environment variables, set 'UNIBEN_WIFI_USERNAME' and
      'UNIBEN_WIFI_PASSWORD' with semicolon-separated values.
      Example:
        UNIBEN_WIFI_USERNAME="username1;username2"
        UNIBEN_WIFI_PASSWORD=";password2"

    - If no credentials are found, the function will raise a NoUserNamePasswordSetError.
    """

    if not username_password:
        username = os.getenv("UNIBEN_WIFI_USERNAME")
        password = os.getenv("UNIBEN_WIFI_PASSWORD")

        if not (username or password):
            raise utils.NoUserNamePasswordSetError()

    # We're guaranteed here that if username_password is None,
    # 'username' and 'password' is defined else an exception would have been raised before we reached this line.

    credentials: List[Tuple[str, str]] = [(u, p,) for u, p in
                                          zip(username.split(";"), password.split(";"))] if not username_password else [
        ((c := username_password.split(";"))[i], c[i + 1],) for i in
        range(0, len(username_password.split(";")), 2)]

    if headless:
        options = Options()
        options.headless = True
        browser = Chrome(options=options)
    else:
        browser = Chrome()
    browser.implicitly_wait(5)

    verdict, i = False, 0

    while verdict is False:
        browser.get(LOGIN_URL)
        try:
            username, password = credentials[i]
            if username is None or password is None:
                print_no_username_password_set_and_quit()
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
                print_invalid_username_or_password_and_quit()
            elif message.startswith("no"):
                verdict = print_execution_failure(message)
            else:
                verdict = False
        except NoSuchElementException:
            break
        except Exception as e:
            print_execution_failure(e)
            quit(0)
        i = (i + 1) % len(credentials)

    print("Logged In Successfully!")


if __name__ == "__main__":
    EXECUTE[len(sys.argv) if len(sys.argv) in EXECUTE else None]()
