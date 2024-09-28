from typing import Union, cast

from gojiparse.rules import (
    BindingPower,
    RuleProvider,
    NullRule,
    LeftRule,
    # StatementRule,
)
from gojiparse.symbols import (
    # symtoken_for_identifier,
    SymbolType,
    SymToken,
)
from gojiparse.parser import Parser

from gojiast.statements import (
    BlockStmt,
    ExpressionStmt,
)
from gojiast.expressions import (
    IntegerExpr,
    FloatExpr,
    BoolExpr,
    StringExpr,
    IdentifierExpr,
    AssignmentExpr,
    BinaryExpr,
    FunctionDefExpr,
    ParamsExpr,
)
from gojiast.interfaces import Expr


from runtime.logging import (
    print_info,
    print_note,
    print_warning,
    print_error,
)


def parse_identifier_expr(p: Parser) -> Union[IdentifierExpr, None]:
    if p.show_parsing:
        print_info("[PIE] parse_identifier_expr()")
        print_info("[PIE] current_token: %s" % p.current_token())
    p.skip_many(SymbolType.LINE_END)
    symtok = p.current_token()
    if symtok is None:
        print_info("[PIE] parse_identifier_expr() without advancing")
        return None
    if p.show_parsing:
        print_info("[PIE] parse_identifier_expr(current_symtok is: %s)" % symtok)
    if symtok.symtype == SymbolType.IDENTIFIER:
        expr = cast(Expr, IdentifierExpr(symtok))
        if p.show_parsing:
            print_info("[PIE] parse_identifier_expr yields: %s)" % expr)

    else:
        expr = None

    if p.show_parsing:
        print("[PIE] WRAPUP parse_identifier_expr()")
        print("[PIE] current_token: %s" % p.current_token())

    p.advance()

    if p.show_parsing:
        print("[PIE] follow_up_token: %s" % p.current_token())

    return cast(IdentifierExpr, expr)


def has_more_params(p: Parser) -> bool:
    sym = p.current_token()
    more_params = True
    if sym is None:
        more_params = False
    elif sym.symtype == SymbolType.RIGHT_PAREN:
        if p.show_parsing:
            print_note("    [HMP] end of params paren found")
        more_params = False

    return more_params


# Positioned at zero or more LINE_END's
# followed by a LEFT_PAREN
def parse_params_expr(p: Parser) -> Union[ParamsExpr, None]:
    if p.show_parsing:
        print_note(">>> [PPE] parse_params_expr()")
        print_note(">>> [PPE] current_token: %s" % p.current_token())
    p.skip_over(SymbolType.LEFT_PAREN)

    # parse 0 or more comma separated args (identifiers, or literals)
    # return None if not a well-formed paramter list
    params: list[IdentifierExpr] = []
    while has_more_params(p):
        if p.show_parsing:
            print_note("    [PPE] Getting another identifier.")
            print_note("    [PPE] current_token is %s" % p.current_token())
        expr = parse_identifier_expr(p)
        if expr is None:
            return None
        symtok = p.current_token()
        if symtok is None:
            return None

        params.append(expr)

        ## Move forward if needed
        p.skip_many(SymbolType.LINE_END)

        ## Update current symbol after potential forwarding
        symtok = p.current_token()
        if p.show_parsing:
            print_note("    [PPE] updated symtok is %s" % symtok)
        if symtok is None:
            return None
        the_type = symtok.symtype
        if p.show_parsing:
            print_note("    [PPE] updated the_type is: %s" % the_type)

        if the_type == SymbolType.COMMA:
            p.skip_over(SymbolType.COMMA)
        elif the_type != SymbolType.RIGHT_PAREN:
            return None

    # return ParamsExpr containing the args.
    if p.show_parsing:
        print_note(
            "    [PPE] wrapping up parse_params_expr.  current_token => %s"
            % p.current_token()
        )

    p.skip_over(SymbolType.RIGHT_PAREN)

    if p.show_parsing:
        print_note(
            "    [PPE] after skipping the RIGHT_PAREN.  current_token => %s"
            % p.current_token()
        )

    return ParamsExpr(params)


# nextsym should be LEFT_PAREN
# sym should be name of function being defined
def parse_fn_def(p: Parser, sym: SymToken) -> Union[Expr, None]:
    if p.show_parsing:
        print_note("")
        print_note(">>> [PFD] parse_fn_def(%s)" % sym.symvalue)

    p.advance()  # makes LEFT_PAREN the current symtok
    params_expr = parse_params_expr(p)  # PH - was left_bp
    if params_expr is None:
        return None
    if p.show_parsing:
        num_params = params_expr.count
        print_note("    [PFD] %d PARAMS for %s" % (num_params, sym.symvalue))
        for idx in range(num_params):
            print_note("    [PFD] %s" % params_expr.param_at_index(idx))
        print_note("    [PFD] updated current_token: %s" % p.current_token())
    p.skip_over(SymbolType.OP_ASSIGN)
    p.skip_many(SymbolType.LINE_END)

    # pylint: disable=fixme
    # TODO: Use something other than parse_expr() here
    body = parse_expr(p, BindingPower.DEFAULT_BP)
    if body is None:
        return None
    block_stmt = BlockStmt(ExpressionStmt(body))

    # HACK: Consumed a LINE_END - need to restore it
    p.backup()

    return FunctionDefExpr(sym, params_expr, block_stmt)


def is_function_def(p: Parser) -> bool:
    next_symtok = p.peek_many(SymbolType.LINE_END)
    if next_symtok is None:
        return False
    next_type = next_symtok.symtype
    return next_type == SymbolType.LEFT_PAREN


# Parser -> ast.Expr
# and advances the parser position
def parse_primary_expr(p: Parser) -> Union[Expr, None]:
    symtok = p.current_token()
    if symtok is None:
        print("[PPR] parse_primary_expr without advancing")
        return None
    if p.show_parsing:
        print("[PPR] parse_primary_expr(%s)" % symtok)

    if symtok.symtype == SymbolType.LITERAL_INTEGER:
        expr = cast(Expr, IntegerExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_FLOAT:
        expr = cast(Expr, FloatExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_BOOL:
        expr = cast(Expr, BoolExpr(symtok))
    elif symtok.symtype == SymbolType.LITERAL_STRING:
        expr = StringExpr(symtok)
    elif symtok.symtype == SymbolType.IDENTIFIER:
        if is_function_def(p):
            maybe_fn_def = parse_fn_def(p, symtok)
            if maybe_fn_def is None:
                expr = cast(Expr, IdentifierExpr(symtok))
            else:
                expr = cast(Expr, maybe_fn_def)
        else:
            expr = cast(Expr, IdentifierExpr(symtok))
        # [PH] if p.show_parsing:
        # [PH]     if nextsymtok is None:
        # [PH]         print("[PPE] nextsymtok is None")
        # [PH]     else:
        # [PH]         print("[PPE] symtok is an IDENTIFIER: %s" % nextsymtok.symvalue)
        # [PH]         print("[PPE] nextsymtok is ", nextsymtok)
        # [PH] if nextsymtok is None:
        # [PH]     expr = cast(Expr, IdentifierExpr(symtok))
        # [PH] else:
        # [PH]     the_type = nextsymtok.symtype
        # [PH]     if the_type == SymbolType.LINE_END:
        # [PH]         expr = cast(Expr, IdentifierExpr(symtok))
        # [PH]     elif the_type == SymbolType.OP_ASSIGN:
        # [PH]         expr = cast(Expr, IdentifierExpr(symtok))
        # [PH]     elif the_type == SymbolType.LEFT_PAREN:
        # [PH]         maybe_fn_def = parse_fn_def(p, symtok)
        # [PH]         if maybe_fn_def is None:
        # [PH]             return None
        # [PH]         else:
        # [PH]             expr = cast(FunctionExpr, maybe_fn_def)
        # [PH]     else:
        # [PH]         expr = cast(Expr, IdentifierExpr(symtok))
    else:
        expr = None
    p.advance()
    return expr


# Parser -> ast.Expr -> BindingPower -> ast.Expr
# and advances the parser position
def parse_binary_expr(
    p: Parser, left_expr: Expr, _left_bp: BindingPower
) -> Union[BinaryExpr, None]:
    operator = p.current_token()
    if operator is None:
        return None
    if p.show_parsing:
        print("parse_binary_expr(%s %s)" % (left_expr, operator))
    rp = p.rule_provider
    operator_bp = rp.bp_for_token_type(operator.symtype)

    p.advance()
    right_expr = parse_expr(p, operator_bp)  # PH - was left_bp
    if right_expr is None:
        print("Unable to parse_expr() to deliver right_expr")
        return None
    return BinaryExpr(operator, left_expr, right_expr)


# Parser -> BindingPower -> ast.Expr
# bp is highest value bp seen so far
# pylint: disable=too-many-return-statements
# pylint: disable=too-many-branches
def parse_expr(p: Parser, overall_bp: BindingPower) -> Union[Expr, None]:
    if p.show_parsing:
        print_info("")
        print_info("parse_expr()")

    symtok = p.current_token()
    if symtok is None:
        return None

    if p.show_parsing:
        print_info("token whose null rule will be sought: %s" % symtok)

    # Check if there is a NullDenoted handler for
    # this type of token
    rp = p.rule_provider
    null_rule = rp.null_rule_for_token_type(symtok.symtype)
    if null_rule is None:
        if not symtok.is_input_end():
            print_warning(
                "ERROR: Expected a symbol with a NullDenoted handler - %s" % symtok
            )
            p.advance_to_sym(SymbolType.LINE_END)
        return None

    if p.show_parsing:
        print("null rule obtained: ", null_rule)

    # Use the null_rule to parse this as the left node
    # (which also will advance the parser pos)
    left_node = null_rule(p)
    if left_node is None:
        print_warning(
            "ERROR: Expected a symbol after applying the NullDenoted handler - %s"
            % p.current_token()
        )
        p.advance_to_sym(SymbolType.LINE_END)
        return None

    symtok = p.current_token()
    if p.show_parsing:
        print_info("Initial left_node (obtained via null_rule): %s" % symtok)

    if symtok is None:
        print("symtok not even provided")
        return left_node

    if symtok.symvalue == SymbolType.LINE_END:
        print("symtok is a LINE_END")
        return left_node

    next_bp = rp.bp_for_token_type(symtok.symtype)

    # Fast-forward to the right, within this expr to find the
    # operator with the highest binding power seen so far
    # for something like "10 + 4" this will fast forward to the 4,
    # but
    while next_bp is not None and (next_bp.value > overall_bp.value):

        left_rule = rp.left_rule_for_token_type(symtok.symtype)
        if left_rule is None:
            print_error(
                "ERROR: Expected a symbol with a LeftDenoted handler - %s" % symtok
            )
            p.advance_to_sym(SymbolType.LINE_END)
            return None

        # Use the left_rule to parse this as the
        # new left node (which incorporates the previous left node)
        # (which also will advance the parser pos)
        left_node = left_rule(p, left_node, overall_bp)
        if left_node is None:
            print_error(
                "ERROR: Expected a symbol after applying the LeftDenoted handler - %s"
                % p.current_token()
            )
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
def parse_assignment_expr(
    p: Parser, left_expr: IdentifierExpr, bp: BindingPower
) -> Union[AssignmentExpr, None]:
    if p.show_parsing:
        print("parse_assignment_expr()")
    p.advance()
    rhs = parse_expr(p, bp)
    if rhs is None:
        return None
    if not isinstance(left_expr, IdentifierExpr):
        return None
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


def init_expr_rules(rp: RuleProvider) -> None:

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
        rp.register_rule(NullRule(bp, x, parse_primary_expr))

    # Math Operations
    rp.register_rule(
        LeftRule(BindingPower.ADDITIVE, SymbolType.OP_ADD, parse_binary_expr)
    )
    rp.register_rule(
        LeftRule(BindingPower.MULTIPLICATIVE, SymbolType.OP_MULTIPLY, parse_binary_expr)
    )

    # Assignment
    rp.register_rule(
        LeftRule(BindingPower.ASSIGNMENT, SymbolType.OP_ASSIGN, parse_assignment_expr)
    )

    # Grouping and Scope
    rp.register_rule(
        NullRule(BindingPower.DEFAULT_BP, SymbolType.LEFT_PAREN, parse_grouping_expr)
    )
