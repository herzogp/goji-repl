import sys
import argparse

# from aug2024.old_program import (
#     old_run_program,
# )

from options import GojiOptions

from program import (
    run_program,
)


def exec_main():
    repl_parser = argparse.ArgumentParser("Goji repl")
    repl_parser.add_argument("program_file", help="Path to Goji program to be run")

    repl_parser.add_argument(
        "-r",
        "--show-rules",
        default=False,
        action="store_true",
        help="Show parsing rules",
    )
    repl_parser.add_argument(
        "-t", "--show-tokens", default=False, action="store_true", help="Show tokens"
    )
    repl_parser.add_argument(
        "-p", "--show-parsing", default=False, action="store_true", help="Show parsing"
    )
    args = repl_parser.parse_args()
    print(args)

    options = GojiOptions(args)
    run_program(options)


def add():
    """Smoke-test for adding two integers.

    Examples:
        Should be executed from a devshell

        >>> $ addx 55 11
        Adding: 55 + 11 => 66
    """
    num1 = 0
    num2 = 0
    if len(sys.argv) > 1:
        maybe_num1 = sys.argv[1]
        if maybe_num1.isdigit():
            num1 = int(maybe_num1)

    if len(sys.argv) > 2:
        maybe_num2 = sys.argv[2]
        if maybe_num2.isdigit():
            num2 = int(maybe_num2)

    the_sum = num1 + num2
    print(f"Adding: {num1} + {num2} => {the_sum}")


if __name__ == "__main__":
    exec_main()
