"""
Utility classes/funcitons module for wifi-bug
"""

from . import USAGE_TEXT


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
    print(
        f"INVALID USERNAME OR PASSWORD!\n"
        f"Try again with correct credentials."
        f"\n\n{USAGE_TEXT}"
    )
    quit(0)


def print_execution_failure(message) -> bool:
    """
    Print execution failure message passed in the argument 'message'
    """
    print(f"{message}")
    return False


class NoUserNamePasswordSetError(Exception):
    """
    Exception to signify that username/password is not set.
    """

    pass
