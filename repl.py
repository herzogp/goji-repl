import argparse

from program import (
    run_program,
)

def exec_main():
    parser = argparse.ArgumentParser("Goji repl")
    parser.add_argument("program_file", help="Path to Goji program to be run")
    args = parser.parse_args()
 

    program_file = args.program_file
    run_program(program_file)


if __name__ == "__main__":
    exec_main()
