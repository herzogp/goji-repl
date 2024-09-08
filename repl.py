import argparse

from old_program import (
    old_run_program,
)

from program import (
    run_program,
)

def exec_main():
    repl_parser = argparse.ArgumentParser("Goji repl")
    repl_parser.add_argument("program_file", help="Path to Goji program to be run")

    repl_parser.add_argument('-n', '--new-parser', default=False, action='store_true', help='Use the new parser')
    repl_parser.add_argument('-P', '--pratt-parser', default=False, action='store_true', help='Use the Pratt parser')
    args = repl_parser.parse_args()
 
    program_file = args.program_file
    print(args)
    wants_new_parser = args.new_parser
    wants_pratt_parser = args.pratt_parser
    which_parser = 'old'
    if wants_new_parser:
        which_parser = 'new'
  
    # wants_pratt_parser
    if wants_pratt_parser:
        run_program(program_file)
    else:
        old_run_program(program_file, which_parser)

if __name__ == "__main__":
    exec_main()
