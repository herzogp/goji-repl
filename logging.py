COLOR_RED = "\033[0;31m"
COLOR_GREEN = "\033[0;32m"
COLOR_BLUE = "\033[0;34m"
COLOR_CYAN = "\033[0;36m"

COLOR_YELLOW = "\033[1;33m"
COLOR_WHITE = "\033[1;37m"
COLOR_ENDC = "\033[0m"

def print_info(s: str) -> None:
    print("%s%s%s" % (COLOR_BLUE, s, COLOR_ENDC))

# An info that should be noticed
def print_note(s: str) -> None:
    print("%s%s%s" % (COLOR_WHITE, s, COLOR_ENDC))

def print_warning(s: str) -> None:
    print("%s%s%s" % (COLOR_YELLOW, s, COLOR_ENDC))

def print_error(s: str) -> None:
    print("%s%s%s" % (COLOR_RED, s, COLOR_ENDC))


