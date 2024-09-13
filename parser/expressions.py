from typing import Union, cast

from parser.rules import (
    BindingPower,
    RuleProvider,
    NullRule,
    LeftRule,
    StatementRule,
)

from parser.symbols import (
    symtoken_for_identifier,
    SymbolType,
    SymToken,
)

from ast.expressions import (
    IntegerExpr,
    FloatExpr,
    BoolExpr,
    StringExpr,
    IdentifierExpr,
    AssignmentExpr,
    BinaryExpr,
    FunctionExpr,
    ParamsExpr,
)


from ast.interfaces import Expr

from parser.parser import Parser

def parse_identifier_expr(p: Parser) -> Union[IdentifierExpr, None]:
    symtok = p.current_token()
    if symtok is None:
        print("parse_identifier_expr without advancing")
        return None
    if p.show_parsing:
        print("parse_identifier_expr(%s)" % symtok)
    if symtok.symtype == SymbolType.IDENTIFIER:
        expr = cast(Expr, IdentifierExpr(symtok))
    else:
        expr = None
    p.advance()
    return expr

def has_more_params(p: Parser) -> bool:
    sym = p.current_token()
    more_params = True
    if sym is None:
        more_params = False
    if sym.symtype == SymbolType.RIGHT_PAREN:
        more_params = False
    if not more_params:
        print("Exhausted params")
    return more_params

# Already seen and advanced 
def parse_params_expr(p: Parser) -> Union[ParamsExpr, None]:
    if p.show_parsing:
        print("parse_params_expr()")
    p.skip_one(SymbolType.LEFT_PAREN)

    # parse 0 or more comma separated args (identifiers, or literals)
    # return None if not a well-formed paramter list
    params: list[IdentifierExpr] = []
    while has_more_params(p):
        expr = parse_identifier_expr(p)
        if expr is None:
            return None
        symtok = p.current_token()
        print("symtok is", symtok)
        if symtok is None:
           return None 
        the_type = symtok.symtype
        print("the_type is:", the_type)
        params.append(expr)
        if the_type == SymbolType.COMMA:
            p.skip_one(SymbolType.COMMA)
        elif the_type != SymbolType.RIGHT_PAREN:
            return None

    # return ParamsExpr containing the args.
    p.skip_one(SymbolType.RIGHT_PAREN)
    return ParamsExpr(params)

def parse_fn_def(p: Parser, sym: SymToken) -> Union[FunctionExpr, None]:
    if p.show_parsing:
        print("parse_fn_def(%s)" % sym)
    # rp = global_rule_provider
    # operator_bp = rp.bp_for_token_type(operator.symtype)
    p.advance() # makes LEFT_PAREN the current symtok
    params_expr = parse_params_expr(p) # PH - was left_bp
    if params_expr is None:
        return None
    print("PARAMS: %s" % params_expr)
    p.skip_one(SymbolType.OP_ASSIGN)

    body = parse_expr(p, BindingPower.DEFAULT_BP)
    if body is None:
        return None
    return FunctionExpr(sym, params_expr, body)

# Parser -> ast.Expr
# and advances the parser position
def parse_primary_expr(p: Parser) -> Union[Expr, None]:
    symtok = p.current_token()
    if symtok is None:
        print("parse_primary_expr without advancing")
        return None
    if p.show_parsing:
        print("parse_primary_expr(%s)" % symtok)

    if symtok.symtype == SymbolType.LITERAL_INTEGER:
        expr = cast(Expr, IntegerExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_FLOAT:
        expr = cast(Expr, FloatExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_BOOL:
        expr = cast(Expr, BoolExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_STRING:
        expr = StringExpr(symtok)
    elif symtok.symtype == SymbolType.IDENTIFIER:
        nextsymtok = p.peek_next_token()
        print("nextsymtok is ", nextsymtok)
        if nextsymtok is None:
            expr = cast(Expr, IdentifierExpr(symtok))
        else:
            the_type = nextsymtok.symtype
            if the_type == SymbolType.LINE_END:
                expr = cast(Expr, IdentifierExpr(symtok))
            elif the_type == SymbolType.OP_ASSIGN:
                expr = cast(Expr, IdentifierExpr(symtok))
            elif the_type == SymbolType.LEFT_PAREN:
                expr = parse_fn_def(p, symtok)
                if expr is None:
                    return None
            else:
                expr = cast(Expr, IdentifierExpr(symtok))
    else:
        expr = None
    p.advance()
    return expr

# Parser -> ast.Expr -> BindingPower -> ast.Expr
# and advances the parser position
def parse_binary_expr(p: Parser, left_expr: Expr, left_bp: BindingPower) -> Union[BinaryExpr, None]:
    operator = p.current_token()
    if operator is None:
        return None
    if p.show_parsing:
        print("parse_binary_expr(%s %s)" % (left_expr, operator))
    rp = global_rule_provider
    operator_bp = rp.bp_for_token_type(operator.symtype)

    p.advance()
    right_expr = parse_expr(p, operator_bp) # PH - was left_bp
    if right_expr is None:
        print("Unable to parse_expr() to deliver right_expr")
        return None
    return BinaryExpr(operator, left_expr, right_expr)

# Parser -> BindingPower -> ast.Expr
# bp is highest value bp seen so far
def parse_expr(p: Parser, overall_bp: BindingPower) -> Union[Expr, None]:
    if p.show_parsing:
        print("parse_expr()")

    symtok = p.current_token()
    if symtok is None:
        return None

    print("token whose null rule will be sought: ", symtok)
    # Check if there is a NullDenoted handler for
    # this type of token
    rp = global_rule_provider
    null_rule = rp.null_rule_for_token_type(symtok.symtype)
    if null_rule is None:
        if not symtok.isinputend():
            print("ERROR: Expected a symbol with a NullDenoted handler - %s" % symtok)
            p.advance_to_sym(SymbolType.LINE_END)
        return None

    print("null rule obtained: ", null_rule)

    # Use the null_rule to parse this as the left node
    # (which also will advance the parser pos)
    left_node = null_rule(p)
    if left_node is None:
        print("ERROR: Expected a symbol after applying the NullDenoted handler - %s" % p.current_token())
        p.advance_to_sym(SymbolType.LINE_END)
        return None

    symtok = p.current_token()
    print("Initial left_node: ", symtok)
    if symtok is None:
        return left_node

    next_bp = rp.bp_for_token_type(symtok.symtype)

    # Fast-forward to the right, within this expr to find the
    # operator with the highest binding power seen so far
    # for something like "10 + 4" this will fast forward to the 4, 
    # but 
    while next_bp != None and (next_bp.value > overall_bp.value):

        left_rule = rp.left_rule_for_token_type(symtok.symtype)
        if left_rule is None:
            print("ERROR: Expected a symbol with a LeftDenoted handler - %s" % symtok)
            p.advance_to_sym(SymbolType.LINE_END)
            return None

        # Use the left_rule to parse this as the 
        # new left node (which incorporates the previous left node)
        # (which also will advance the parser pos)
        left_node = left_rule(p, left_node, overall_bp)
        if left_node is None:
            print("ERROR: Expected a symbol after applying the LeftDenoted handler - %s" % p.current_token())
            p.advance_to_sym(SymbolType.LINE_END)
            return None

        # Since the parser has been advanced,
        # get the new current_token
        symtok = p.current_token()
        if symtok is None:
            return left_node
        next_bp = rp.bp_for_token_type(symtok.symtype)

    return left_node

# Parser -> ast.Expr -> BindingPower -> ast.Expr
def parse_assignment_expr(p: Parser, left_expr: IdentifierExpr, bp: BindingPower) -> Union[AssignmentExpr, None]:
    if p.show_parsing:
        print("parse_assignment_expr()")
    p.advance()
    rhs = parse_expr(p, bp)
    if rhs is None:
        return None
    if not isinstance(left_expr, IdentifierExpr):
        return None
        # print("?? IdentifierExpr ?? ", left_expr)
        # id_name_symtoken = symtoken_for_identifier('_')
    else:
        id_name_symtoken = left_expr.name
    expr_node = AssignmentExpr(id_name_symtoken, rhs)
    return expr_node

# Parser -> ast.Expr
def parse_grouping_expr(p: Parser) -> Union[Expr, None]:
    p.skip_one(SymbolType.LEFT_PAREN)
    grouped_expr = parse_expr(p, BindingPower.DEFAULT_BP)
    if grouped_expr is None:
        return None
    p.skip_one(SymbolType.RIGHT_PAREN)
    return grouped_expr

def create_rule_provider() -> RuleProvider:

    rule_provider = RuleProvider()

    # Literals & Symbols
    all_literals = [
        SymbolType.LITERAL_INTEGER,
        SymbolType.LITERAL_FLOAT,
        SymbolType.LITERAL_STRING,
        SymbolType.LITERAL_BOOL,
        SymbolType.IDENTIFIER,
    ]
    bp = BindingPower.PRIMARY
    for x in all_literals:
        rule_provider.register_rule(NullRule(bp, x, parse_primary_expr))

    # Math Operations
    rule_provider.register_rule(LeftRule(BindingPower.ADDITIVE, SymbolType.OP_ADD, parse_binary_expr))
    rule_provider.register_rule(LeftRule(BindingPower.MULTIPLICATIVE, SymbolType.OP_MULTIPLY, parse_binary_expr))

    # Assignment
    rule_provider.register_rule(LeftRule(BindingPower.ASSIGNMENT, SymbolType.OP_ASSIGN, parse_assignment_expr))

    # Grouping and Scope
    rule_provider.register_rule(NullRule(BindingPower.DEFAULT_BP, SymbolType.LEFT_PAREN, parse_grouping_expr))

    return rule_provider

global_rule_provider = create_rule_provider()

