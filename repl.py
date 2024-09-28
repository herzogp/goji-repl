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


if __name__ == "__main__":
    exec_main()
