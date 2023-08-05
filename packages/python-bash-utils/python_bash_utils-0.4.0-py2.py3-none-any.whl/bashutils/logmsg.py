from colorama import Fore, Style
from colorama import init as colorama_init

colorama_init(autoreset=True)

# Fore: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Back: BLACK, RED, GREEN, YELLOW, BLUE, MAGENTA, CYAN, WHITE, RESET.
# Style: DIM, NORMAL, BRIGHT, RESET_ALL

# BRIGHT_WHITE = Fore.WHITE + Style.BRIGHT

# -----------------------------------------------------------------------------
# User feedback
# -----------------------------------------------------------------------------


def divline(count=80):
    """Prints a divider line."""
    value = "-" * count
    print(value)


def header(string):
    """Prints a header."""
    value = f"{Fore.GREEN}==> {Fore.WHITE}{Style.BRIGHT}{string}"
    print(value)


def success(string):
    """Prints a success message."""
    value = f"{Fore.GREEN}[OK] {Fore.WHITE}{string}"
    print(value)


def error(string):
    """Prints a error message."""
    value = f"{Fore.RED}[ERROR] {Fore.WHITE}{string}"
    print(value)


def warning(string):
    """Prints a warning message."""
    value = f"{Fore.YELLOW}[WARNING] {Fore.WHITE}{string}"
    print(value)


def info(string):
    """Prints a info message."""
    value = f"{Fore.CYAN}[INFO] {string}"
    print(value)


def note(string):
    """Prints a note message."""
    value = Style.DIM + string
    print(value)


# -----------------------------------------------------------------------------
# User Input
# -----------------------------------------------------------------------------


def prompt(question):
    """Prompts user for input."""
    return input(f"[?] {question}: ")


def confirm(question):
    """Prompts user to confirm with (y/n)."""
    response = input(f"[?] {question}? (y/n) ")
    return response.lower() in ["y", "yes"]

# -----------------------------------------------------------------------------


class Console:
    """Simple class to aid in code completion."""

    @staticmethod
    def header(msg):
        return header(msg)

    @staticmethod
    def success(msg):
        return success(msg)

    @staticmethod
    def error(msg):
        return error(msg)

    @staticmethod
    def warning(msg):
        return warning(msg)

    @staticmethod
    def info(msg):
        return info(msg)

    @staticmethod
    def note(msg):
        return note(msg)

    @staticmethod
    def prompt(question):
        """Prompts user for input."""
        return prompt(question)

    @staticmethod
    def confirm(question):
        """Prompts user to confirm with (y/n)."""
        return confirm(question)

# -----------------------------------------------------------------------------

if __name__ == "__main__":
    divline()
    header("Header")
    success("Success")
    error("Error")
    warning("Warning")
    info("Info")
    note("Note goes here")

    name = prompt("What is your name?")
    success(name)

    if confirm("Confirm this"):
        success("You confirmed!")
