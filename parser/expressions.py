from parser.rules import (
    BindingPower,
    null_rule_for_token_type,
    left_rule_for_token_type,
)

from parser.symbols import (
    SymbolType,
)

# Parser -> ast.Expr
# and advances the parser position
def parse_primary_expr(p):
    symtok = p.current_token()
    expr = None
    if symtok.symtype == SymbolType.LITERAL_INTEGER:
        expr = IntegerExpr(symtok.symvalue)
    elif symtok.symtype == SymbolType.LITERAL_FLOAT:
        expr = FloatExpr(symtok.symvalue)
    elif symtok.symtype == SymbolType.LITERAL_BOOL:
        expr = BoolExpr(symtok.symvalue)
    elif symtok.symtype == SymbolType.LITERAL_STRING:
        expr = StringExpr(symtok.symvalue)
    elif symtok.symtype == SymbolType.IDENTIFIER:
        expr = IdentifierExpr(symtok.symvalue)
    else:
        expr = None
    p.advance()
    return expr

# Parser -> ast.Expr -> BindingPower -> ast.Expr
# and advances the parser position
def parse_binary_expr(p, left_expr, left_bp):
    operator = p.current_token()
    operator_bp = bp_for_token_type(operator.symtype)
    p.advance()
    right_expr = parse_expr(p, operator_bp) # PH - was left_bp
    return BinaryExpr(operator, left_expr, right_expr)

# Parser -> BindingPower -> ast.Expr
# bp is highest value bp seen so far
def parse_expr(p, overall_bp):

    symtok = p.current_token()

    # Check if there is a NullDenoted handler for
    # this type of token
    null_rule = null_rule_for_token_type(symtok.symtype)
    if null_rule == None:
        print("ERROR: Expected a symbol with a NullDenoted handler - %s" % symtok)
        return None

    # Use the null_rule to parse this as the left node
    # (which also will advance the parser pos)
    left_node = null_rule(p)

    symtok = p.current_token()
    next_bp = bp_for_token_type(symtok.symtype)

    # Fast-forward to the right, within this expr to find the
    # operator with the highest binding power seen so far
    # for something like "10 + 4" this will fast forward to the 4, 
    # but 
    while next_bp > overall_bp:
        left_rule = left_rule_for_token_type(symtok.symtype)
        if left_rule == None:
            print("ERROR: Expected a symbol with a LeftDenoted handler - %s" % symtok)
            return None
        # Use the left_rule to parse this as the 
        # new left node (which incorporates the previous left node)
        # (which also will advance the parser pos)
        new_left_node = left_rule(p, left_node, overall_bp)
        left_node = new_left_node

        # Since the parser has been advanced,
        # get the new current_token
        symtok = p.current_token()
        next_bp = bp_for_token_type(symtok.symtype)

    return left_node

# Parser -> ast.Expr -> BindingPower -> ast.Expr
def parse_assignment_expr(p, left_expr, bp):
    # Why do we advance immediately?
    # Is it to 'ignore' the 'Let' keyword?
    p.advance()

    rhs = parse_expr(p, bp)
    expr_node = AssignmentExpr(left, rhs)
    return expr_node

# Parser -> ast.Expr
def parse_grouping_expr(p):
    p.skip_one(SymbolType.LEFT_PAREN)
    grouped_expr = parse_expr(p, BindingPower.DEFAULT_BP)
    p.skip_one(SymbolType.RIGHT_PAREN)
    return grouped_expr

