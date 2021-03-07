import sys


def print_error(message: str):
    print(f"[ ERROR ] {message}")


def print_error_and_stop(message: str):
    print_error(message)
    sys.exit(1)


def print_warning(message: str):
    print(f"[WARNING] {message}")


def print_info(message: str):
    print(f"[ INFO  ] {message}")
