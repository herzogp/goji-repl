import argparse 

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
  
    # wants_pratt_parser
    which_parser = 'old'
    if wants_pratt_parser:
        which_parser = 'pratt'
    else:
        if wants_new_parser:
            which_parser = 'new'

    run_program(program_file, which_parser)


if __name__ == "__main__":
    exec_main()
