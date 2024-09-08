from enum import Enum

from parser.driver import (
    pratt_parse_program,
)

from ast.expressions import (
    StringExpr,
    IntegerExpr,
    BoolExpr,
)

from runtime.env import (
    EnvItem,
    EnvTable,
)

from runtime.eval import (
    eval_stmt,
)

from parser.symbols import (
    symtoken_for_numeric,
    symtoken_for_text,
    symtoken_for_identifier,
)

class EngineVersion(Enum):
    V0_2_0 = 10

def run_program(program_file):
    # Setup the root environment
    program_env = EnvTable()

    # Add the engine version
    name_val = EngineVersion.V0_2_0.name
    # builtin = EnvItem('engineVersion-name', make_atom_node(Token.QTEXT, EngineVersion.V0_2_0.name))
    builtin = EnvItem('engineVersion-name', StringExpr(symtoken_for_text(EngineVersion.V0_2_0.name)))
    program_env.set_item(builtin)

    this_val = EngineVersion.V0_2_0.value
    builtin = EnvItem('engineVersion-id', IntegerExpr(symtoken_for_numeric(str(EngineVersion.V0_2_0.value))))
    program_env.set_item(builtin)

    builtin = EnvItem('seven_eleven', IntegerExpr(symtoken_for_numeric(str(711))))
    program_env.set_item(builtin)

    builtin = EnvItem('true', BoolExpr(symtoken_for_identifier('true')))
    program_env.set_item(builtin)
    
    builtin = EnvItem('false', BoolExpr(symtoken_for_identifier('false')))
    program_env.set_item(builtin)

    # parse and show/eval AST
    all_statements = pratt_parse_program(program_file)

    # Time to evaluate
    if all_statements == None:
        print("Nothing to evaluate")
    else:
        print("%d statements will be evaluated" % len(all_statements))
        for stmt in all_statements:
            print("[%2d] %s" % (stmt.line, stmt))
            result = eval_stmt(program_env, stmt) 
            print("==> %s" % result)
            print("")

    # show ending environment
    print("\nGoji Ending Environment:")
    program_env.show()

