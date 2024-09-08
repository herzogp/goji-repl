# statement.py
from parser.rules import (
    BindingPower,
)

from parser.expressions import (
    parse_expr,
)

from ast.statements import (
    ExpressionStmt,
)

from parser.symbols import SymbolType

# Parser -> ast.Stmt
def parse_statement(p):
    symtok = p.current_token()
    rp = p.rule_provider
    statement_rule = rp.statement_rule_for_token_type(symtok.symtype)
    if statement_rule != None:
        return statement_rule(p)

    expression = parse_expr(p, BindingPower.DEFAULT_BP)
    p.skip_one(SymbolType.LINE_END)    
    return ExpressionStmt(expression)
