from typing import Union, cast

from parser.rules import (
    BindingPower,
    RuleProvider,
    NullRule,
    LeftRule,
    StatementRule,
)

from parser.symbols import (

    SymbolType,
)

from ast.expressions import (
    IntegerExpr,
    FloatExpr,
    BoolExpr,
    StringExpr,
    IdentifierExpr,
    AssignmentExpr,
    BinaryExpr,
)

from ast.interfaces import Expr

from parser.parser import Parser

# Parser -> ast.Expr
# and advances the parser position
def parse_primary_expr(p: Parser) -> Union[Expr, None]:
    print("parse_primary_expr()")
    symtok = p.current_token()
    if symtok is None:
        print("parse_primary_expr without advancing")
        return None
    if symtok.symtype == SymbolType.LITERAL_INTEGER:
        expr = cast(Expr, IntegerExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_FLOAT:
        expr = cast(Expr, FloatExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_BOOL:
        expr = cast(Expr, BoolExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_STRING:
        expr = StringExpr(symtok)
    elif symtok.symtype == SymbolType.IDENTIFIER:
        expr = cast(Expr, IdentifierExpr(symtok))
    else:
        expr = None
    p.advance()
    return expr

# Parser -> ast.Expr -> BindingPower -> ast.Expr
# and advances the parser position
def parse_binary_expr(p: Parser, left_expr: Expr, left_bp: Expr) -> Union[BinaryExpr, None]:
    print("parse_binary_expr()")
    operator = p.current_token()
    if operator is None:
        return None
    rp = global_rule_provider
    # [PH] rp = p.rule_provider
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
    print("parse_expr()")

    symtok = p.current_token()
    if symtok is None:
        return None

    # Check if there is a NullDenoted handler for
    # this type of token
    rp = global_rule_provider
    # rp.show_all_rules()
    # [PH] rp = p.rule_provider
    #
    null_rule = rp.null_rule_for_token_type(symtok.symtype)
    if null_rule is None:
        print("ERROR: Expected a symbol with a NullDenoted handler - %s" % symtok)
        p.advance()
        return None

    # Use the null_rule to parse this as the left node
    # (which also will advance the parser pos)
    left_node = null_rule(p)
    print("Applied the null_rule to provide left_node: ", left_node)

    symtok = p.current_token()
    if symtok is None:
        return left_node

    next_bp = rp.bp_for_token_type(symtok.symtype)

    # Fast-forward to the right, within this expr to find the
    # operator with the highest binding power seen so far
    # for something like "10 + 4" this will fast forward to the 4, 
    # but 
    while next_bp != None and (next_bp.value > overall_bp.value):

        print("next_bp: ", next_bp)
        print("call left_rule_for_token_type on symtok: ", symtok)
        print("symtok.symtype is: ", symtok.symtype)

        left_rule = rp.left_rule_for_token_type(symtok.symtype)
        if left_rule is None:
            print("ERROR: Expected a symbol with a LeftDenoted handler - %s" % symtok)
            return None

        # Use the left_rule to parse this as the 
        # new left node (which incorporates the previous left node)
        # (which also will advance the parser pos)
        left_node = left_rule(p, left_node, overall_bp)

        # Since the parser has been advanced,
        # get the new current_token
        symtok = p.current_token()
        if symtok is None:
            return left_node
        next_bp = rp.bp_for_token_type(symtok.symtype)

    return left_node

# Parser -> ast.Expr -> BindingPower -> ast.Expr
def parse_assignment_expr(p: Parser, left_expr: IdentifierExpr, bp: BindingPower) -> Union[AssignmentExpr, None]:
    print("parse_assignment_expr()")
    p.advance()
    rhs = parse_expr(p, bp)
    if rhs is None:
        return None
    expr_node = AssignmentExpr(left_expr.name, rhs)
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

