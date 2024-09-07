from ast.expressions import (
    AssignmentExpr,
    IdentifierExpr,
    BinaryExpr,
)

from parser.symbols import SymbolType

from ast.statements import (
    ExpressionStmt,
)

def eval_expr(env, expr):
    if isinstance(expr, AssignmentExpr):
        print("Assign %s <= '%s'" % (expr.ident.value, expr.rhs))
    elif isinstance(expr, IdentifierExpr):
        print("Dereference %s" % expr.value)
    elif isinstance(expr, BinaryExpr):
        operator = expr.operator
        opsym = operator.symtype
        if opsym == SymbolType.OP_ADD:
            print("Add values")
        elif expr.opsym == SymbolType.OP_MULTIPLY:
            print("Multiply values")
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
