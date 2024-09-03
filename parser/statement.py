# statement.py

Parser -> ast.Stmt
def parse_statement(p):
    symtok = p.current_token()
    statement_rule = statement_rule_for_token_type()
    if statement_rule != None:
        return statement_rule(p)

    expression = parse_expr(p, BindingPower.DEFAULT_BP)
    p.expect(SymToken.LINE_END)    
    return ast.ExpressionStatement(expression)
