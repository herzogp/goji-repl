import argparse 

from program import (
    run_program,
)

def exec_main():
    parser = argparse.ArgumentParser("Goji repl")
    parser.add_argument("program_file", help="Path to Goji program to be run")

    parser.add_argument('-n', '--new-parser', default=False, action='store_true', help='Use the new parser')
    args = parser.parse_args()
 

    program_file = args.program_file
    print(args)
    new_parser = args.new_parser
    run_program(program_file, new_parser)


if __name__ == "__main__":
    exec_main()
