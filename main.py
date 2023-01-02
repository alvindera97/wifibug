import sys
from typing import NoReturn, Dict, Callable, Optional

EXECUTE: Dict[Optional[int], Callable] = {
    2: lambda: main(
        headless=True if sys.argv[1] == "headless" else False),
    4: lambda: main(
        headless=True if sys.argv[1] == "headless" else False,
        username=sys.argv[2],
        password=sys.argv[3]),
    None: lambda: print(
        f"USAGE: python main.py [headless/visual] [username password]")
}


class NoUsernamePasswordSetError(Exception):
    pass


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


if __name__ == "__main__":
    EXECUTE[len(sys.argv) if len(sys.argv) in EXECUTE else None]()
    print(len(sys.argv))
