from typing import NoReturn


class NoUsernamePasswordSetError(Exception): pass


def main(headless: bool = False, username: str = None, password: str = None) -> NoReturn:
    """
    Persistently try to login to UNIBEN wifi given username and password.

    If username and password is given, then given username and password combinations are used login,
    if given username and password combinations are incorrect however, main() fails instantly displaying the error

    If username and password aren't given, environment variables storing "UNIBEN_WIFI_USERNAME' and 'UNIBEN_WIFI_PASSWORD'
    are used as credentials.
    If no environment variable for 'UNIBEN_WIFI_USERNAME' and [or] 'UNIBEN_WIFI_PASSWORD' exist, main() raises NoUsernamePasswordSetError
    It's following operation is the same as if username and password were originally given.
    """
    pass
