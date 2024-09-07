from ast.expressions import (
    AssignmentExpr,
    IdentifierExpr,
    BinaryExpr,
    IntegerExpr,
    FloatExpr,
    BoolExpr,
    StringExpr,
)

from parser.symbols import SymbolType

from ast.statements import (
    ExpressionStmt,
)

def eval_expr(env, expr):
    if isinstance(expr, AssignmentExpr):
        result = eval_expr(env, expr.rhs)
        print("Assign %s <= %s" % (expr.ident.value, str(result)))
        return result
    elif isinstance(expr, IntegerExpr):
        # print("Integer %d" % expr.value)
        return expr.value
    elif isinstance(expr, FloatExpr):
        # print("Float %g" % expr.value)
        return expr.value
    elif isinstance(expr, StringExpr):
        # print("String %s" % expr.value)
        return expr.value
    elif isinstance(expr, BoolExpr):
        # print("Bool %b" % expr.value)
        return expr.value
    elif isinstance(expr, IdentifierExpr):
        print("Dereference %s" % expr.value)
        return 3297  #expr.value
    elif isinstance(expr, BinaryExpr):
        operator = expr.operator
        opsym = operator.symtype
        lhs = eval_expr(env, expr.lhs)
        rhs = eval_expr(env, expr.rhs)
        if opsym == SymbolType.OP_ADD:
            print("Add values: %d + %d" % (lhs, rhs))
            result = lhs + rhs
            return result
        elif opsym == SymbolType.OP_MULTIPLY:
            print("Multiply values: %d * %d" % (lhs, rhs))
            result = lhs * rhs
            return result
    else:
        print("Another expr named: %s" % type(expr))
    return None

def eval_other(env, other):
    print("Evaluating [%2d] %s" % (stmt.line, other))
    return None


def eval_stmt(env, stmt):
    # print("Evaluating [%2d] %s" % (stmt.line, stmt))
    if isinstance(stmt, ExpressionStmt):
        return eval_expr(env, stmt.expression)
    else:
        return eval_other(env, stmt)
