from enum import Enum

from env import (
    EnvItem,
    EnvTable,
)

from eval import (
    eval_node,
)

from old_parser import (
    parse_program,
    new_parse_program,
)

from atom import (
    Atom,
    Builtin,
)

from node import (
    make_atom_node,
    make_node_from_atom,
)

from tokenizer import (
    Token,
    TokenItem,
)

class EngineVersion(Enum):
    V0_1_0 = 3

def isOldParser(which_parser):
    return which_parser == 'old'

def isNewParser(which_parser):
    return which_parser == 'new'

def isPrattParser(which_parser):
    return which_parser == 'pratt'

def run_program(program_file, which_parser):
    # Setup the root environment
    program_env = EnvTable()

    # Add the engine version
    name_val = EngineVersion.V0_1_0.name
    builtin = EnvItem('engineVersion-name', make_atom_node(Token.QTEXT, EngineVersion.V0_1_0.name))
    program_env.set_item(builtin)

    this_val = EngineVersion.V0_1_0.value
    builtin = EnvItem('engineVersion-id', make_atom_node(Token.NUMERIC, str(EngineVersion.V0_1_0.value)))
    program_env.set_item(builtin)

    builtin = EnvItem('seven', make_atom_node(Token.NUMERIC, str(7)))
    program_env.set_item(builtin)

    temp_atom = Atom(TokenItem(Token.QTEXT, 'true')).asbool()
    builtin = EnvItem('true', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)
    
    temp_atom = Atom(TokenItem(Token.QTEXT, 'false')).asbool()
    builtin = EnvItem('false', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)

    temp_atom = Atom(TokenItem(Token.QTEXT, '=')).asbuiltin()
    builtin = EnvItem('=', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)

    temp_atom = Atom(TokenItem(Token.QTEXT, '+')).asbuiltin()
    builtin = EnvItem('+', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)

    temp_atom = Atom(TokenItem(Token.QTEXT, '*')).asbuiltin()
    builtin = EnvItem('*', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)

    # parse and show/eval AST
    all_nodes = None
    if isPrattParser(which_parser):
        print("Would use Pratt Parser")
    elif isNewParser(which_parser):
        all_nodes = new_parse_program(program_file)
    else:
        all_nodes = parse_program(program_file)

    # Time to evaluate
    if all_nodes == None:
        print("Nothing to evaluate")
    else:
        print("%d nodes will be evaluated" % len(all_nodes))
        for idx, n in enumerate(all_nodes):
            print("\n[%2.2i] %s" % (idx, str(n)))
            node_val = eval_node(program_env, n)
            print("=> %s" % str(node_val))

 
    # show ending environment
    print("\nGoji Ending Environment:")
    program_env.show()
