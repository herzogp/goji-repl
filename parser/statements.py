# statement.py

from typing import Union

from parser.rules import (
    BindingPower,
    StmtHandler,
)

from parser.expressions import (
    parse_expr,
    global_rule_provider,
)

from ast.statements import (
    ExpressionStmt,
)

from ast.interfaces import Stmt

from parser.driver import Parser

from parser.symbols import SymbolType

# Parser -> ast.Stmt
def parse_statement(p: Parser, source_line: str) -> Union[Stmt, None]:
    symtok = p.current_token()
    if symtok is None:
        return None
    rp = global_rule_provider
    stmt_rule = rp.statement_rule_for_token_type(symtok.symtype)
    if stmt_rule is None:
        line_number = symtok.line
        expression = parse_expr(p, BindingPower.DEFAULT_BP)
        p.skip_one(SymbolType.LINE_END)    
        if (expression is None): # or (symtok.isinputend()):
            # print("Xym: ", symtok)
            if line_number > 0:
                print("[%2d] %s" % (line_number, source_line))
                print("")
            return None
        # p.skip_one(SymbolType.LINE_END)    
        return ExpressionStmt(expression)
    return stmt_rule(p)
