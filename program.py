from enum import Enum

from env import (
    EnvItem,
    EnvTable,
    ItemType,
)

from eval import (
    eval_node,
)

from parser import (
    parse_program,
)

from atom import (
    Builtin,
)

class EngineVersion(Enum):
    V0_1_0 = 3,

def run_program(program_file):
    # Setup the root environment
    program_env = EnvTable()

    # Add the engine version
    builtin = EnvItem('engineVersion-id', ItemType.INTEGER, EngineVersion.V0_1_0.value)
    program_env.set_item(builtin)
    builtin = EnvItem('engineVersion-name', ItemType.TEXT, (EngineVersion.V0_1_0.name,))
    program_env.set_item(builtin)

    builtin = EnvItem('define', ItemType.FUNCTION, (Builtin.DEFINE,))
    program_env.set_item(builtin)

    builtin = EnvItem('+', ItemType.FUNCTION, (Builtin.OP_PLUS,))
    program_env.set_item(builtin)

    builtin = EnvItem('*', ItemType.FUNCTION, (Builtin.OP_MULT,))
    program_env.set_item(builtin)

    builtin = EnvItem('seven', ItemType.INTEGER, (7,))
    program_env.set_item(builtin)

    builtin = EnvItem('#t', ItemType.BOOL, (True,))
    program_env.set_item(builtin)

    builtin = EnvItem('#f', ItemType.BOOL, (False,))
    program_env.set_item(builtin)

    # parse and show/eval AST
    all_nodes = parse_program(program_file)
    for idx, n in enumerate(all_nodes):
        print("\n[%2.2i] %s" % (idx, str(n)))
        tk_item = eval_node(program_env, n)
        print("=> %s" % str(tk_item))
 
    # show ending environment
    print("\nGoji Ending Environment:")
    program_env.show()
