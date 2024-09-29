from enum import Enum

from gojiparse.driver import pratt_parse_program
from gojiparse.symbols import (
    symtoken_for_numeric,
    symtoken_for_text,
    symtoken_for_identifier,
)


from gojiast.expressions import (
    StringExpr,
    IntegerExpr,
    BoolExpr,
)

from options import GojiOptions

from runtime.env import (
    EnvItem,
    EnvTable,
)

from runtime.eval import (
    eval_stmt,
)


class EngineVersion(Enum):
    V0_2_0 = 10


def run_program(options: GojiOptions) -> None:
    program_file = options.program_file

    # Setup the root environment
    program_env = EnvTable()

    # Add the engine version
    name_val = EngineVersion.V0_2_0.name
    builtin = EnvItem("engineVersion-name", StringExpr(symtoken_for_text(name_val)))
    program_env.set_item(builtin)

    this_val = EngineVersion.V0_2_0.value
    builtin = EnvItem(
        "engineVersion-id",
        IntegerExpr(symtoken_for_numeric(str(this_val))),
    )
    program_env.set_item(builtin)

    builtin = EnvItem("seven_eleven", IntegerExpr(symtoken_for_numeric(str(711))))
    program_env.set_item(builtin)

    builtin = EnvItem("true", BoolExpr(symtoken_for_identifier("true")))
    program_env.set_item(builtin)

    builtin = EnvItem("false", BoolExpr(symtoken_for_identifier("false")))
    program_env.set_item(builtin)

    # parse and show/eval AST
    all_statements, all_lines = pratt_parse_program(program_file, options)

    # Time to evaluate
    if all_statements is None:
        print("Nothing to evaluate")
    else:
        # print("%d statements will be evaluated" % len(all_statements))
        for stmt in all_statements:
            lno = stmt.line
            print("[%2d] %s" % (lno, all_lines[lno - 1]))
            result = eval_stmt(program_env, stmt)
            if result is None:
                print("==> Runtime Error")
            else:
                print("==> %s" % result)
            print("")

    # show ending environment
    print("\nGoji Ending Environment:")
    program_env.show()
