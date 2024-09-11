from typing import Union, cast

from ast.interfaces import Expr

from ast.expressions import (
    AssignmentExpr,
    IdentifierExpr,
    BinaryExpr,
    IntegerExpr,
    FloatExpr,
    BoolExpr,
    StringExpr,
    BaseExpr,
)

from parser.symbols import (
    SymbolType,
    SymToken,
    symtoken_for_numeric,
)

from ast.statements import (
    ExpressionStmt,
)

from runtime.env import (
    EnvItem,
)

def eval_expr(env, expr) -> Union[Expr, None]:
    if isinstance(expr, AssignmentExpr):
        result = eval_expr(env, expr.rhs)
        ident_expr = expr.ident
        item_name = ident_expr.name.symvalue
        item = EnvItem(item_name, result)
        env.set_item(item)
        return result
    elif isinstance(expr, IntegerExpr):
        return expr
    elif isinstance(expr, FloatExpr):
        return expr
    elif isinstance(expr, StringExpr):
        return expr
    elif isinstance(expr, BoolExpr):
        return expr
    elif isinstance(expr, IdentifierExpr):
        maybe_item = env.get_item(expr.name.symvalue)
        return maybe_item.value
    elif isinstance(expr, BinaryExpr):
        operator = expr.operator
        opsym = operator.symtype
        lhs = cast(BaseExpr, eval_expr(env, expr.lhs))
        rhs = cast(BaseExpr, eval_expr(env, expr.rhs))
        leftval = lhs.exprvalue
        rightval = rhs.exprvalue
        lefttype = lhs.exprtype
        righttype = rhs.exprtype
        if opsym == SymbolType.OP_ADD:
            print("Add values: %g + %g" % (float(leftval), float(rightval)))
            result = leftval + rightval
            if (lefttype == SymbolType.LITERAL_INTEGER) and (righttype == SymbolType.LITERAL_INTEGER):
                return IntegerExpr(symtoken_for_numeric(result))
            else:
                return FloatExpr(symtoken_for_numeric(result))
        elif opsym == SymbolType.OP_MULTIPLY:
            print("Multiply values: %g * %g" % (float(leftval), float(rightval)))
            result = leftval * rightval
            if (lefttype == SymbolType.LITERAL_INTEGER) and (righttype == SymbolType.LITERAL_INTEGER):
                return IntegerExpr(symtoken_for_numeric(result))
            else:
                return FloatExpr(symtoken_for_numeric(result))
    else:
        print("Another expr named: %s" % type(expr))
    return None

def eval_other(env, other) -> None:
    print("Evaluating [%2d] %s" % (stmt.line, other))
    return None


def eval_stmt(env, stmt) -> Union[Expr, None]:
    if isinstance(stmt, ExpressionStmt):
        return eval_expr(env, stmt.expression)
    else:
        return eval_other(env, stmt)
