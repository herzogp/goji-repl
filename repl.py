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

    # repl_parser.add_argument('-n', '--new-parser', default=False, action='store_true', help='Use the new parser')
    # repl_parser.add_argument('-P', '--pratt-parser', default=False, action='store_true', help='Use the Pratt parser')
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

    program_file = args.program_file
    print(args)
    # wants_pratt_parser = args.pratt_parser
    # wants_new_parser = args.new_parser
    # which_parser = 'old'
    # if wants_new_parser:
    #     which_parser = 'new'

    # wants_pratt_parser
    # if wants_pratt_parser:
    #     run_program(program_file)
    # else:
    #     old_run_program(program_file, which_parser)
    #
    options = GojiOptions(args)

    run_program(options)


if __name__ == "__main__":
    exec_main()
