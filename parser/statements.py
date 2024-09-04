# statement.py
from parser.rules import (
    BindingPower,
    statement_rule_for_token_type,
)

from parser.expressions import (
    parse_expr,
)

from parser.symbols import SymbolType

# Parser -> ast.Stmt
def parse_statement(p):
    symtok = p.current_token()
    statement_rule = statement_rule_for_token_type(symtok.symtype)
    if statement_rule != None:
        return statement_rule(p)

    expression = parse_expr(p, BindingPower.DEFAULT_BP)
    p.skip_one(SymbolType.LINE_END)    
    return ast.ExpressionStatement(expression)
