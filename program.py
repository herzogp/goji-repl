from enum import Enum

from env import (
    EnvItem,
    EnvTable,
)

from eval import (
    eval_node,
)

from parser import (
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

def run_program(program_file, new_parser):
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

    temp_atom = Atom(TokenItem(Token.QTEXT, 'define')).asbuiltin()
    builtin = EnvItem('define', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)

    temp_atom = Atom(TokenItem(Token.QTEXT, '+')).asbuiltin()
    builtin = EnvItem('+', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)

    temp_atom = Atom(TokenItem(Token.QTEXT, '*')).asbuiltin()
    builtin = EnvItem('*', make_node_from_atom(temp_atom))
    program_env.set_item(builtin)

    # parse and show/eval AST
    if new_parser:
        all_nodes = new_parse_program(program_file)
    else:
        all_nodes = parse_program(program_file)

    if not new_parser:
        for idx, n in enumerate(all_nodes):
            print("\n[%2.2i] %s" % (idx, str(n)))
            node_val = eval_node(program_env, n)
            print("=> %s" % str(node_val))
 
    # show ending environment
    print("\nGoji Ending Environment:")
    program_env.show()
