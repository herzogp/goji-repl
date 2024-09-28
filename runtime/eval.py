from typing import Union, cast

from ast.interfaces import Expr, Stmt

from ast.expressions import (
    AssignmentExpr,
    IdentifierExpr,
    BinaryExpr,
    IntegerExpr,
    FloatExpr,
    BoolExpr,
    StringExpr,
    BaseExpr,
    FunctionDefExpr,
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
    EnvTable,
    nil_expr,
)


class NumericOperands:
    def __init__(self, lhs: BaseExpr, rhs: BaseExpr) -> None:
        leftval = lhs.exprvalue
        rightval = rhs.exprvalue
        lefttype = lhs.exprtype
        righttype = rhs.exprtype
        self._are_float = True
        self._are_valid = True
        if lefttype == SymbolType.LITERAL_INTEGER:
            if righttype == SymbolType.LITERAL_INTEGER:
                self._left_int = cast(int, leftval)
                self._right_int = cast(int, rightval)
                self._are_float = False
            elif righttype == SymbolType.LITERAL_FLOAT:
                self._left_float = float(cast(int, leftval))
                self._right_float = cast(float, rightval)
        elif lefttype == SymbolType.LITERAL_FLOAT:
            self._left_float = cast(float, leftval)
            if righttype == SymbolType.LITERAL_FLOAT:
                self._right_float = cast(float, rightval)
            elif righttype == SymbolType.LITERAL_INTEGER:
                self._right_float = float(cast(int, rightval))
            else:
                print("Type mismatch: %s + %s" % (lhs, rhs))
                return None
        else:
            self._are_float = False
            self._are_valid = False

    @property
    def are_valid(self) -> bool:
        return self._are_valid

    @property
    def are_float(self) -> bool:
        return self._are_valid and self._are_float

    @property
    def left_float(self) -> float:
        return self._left_float

    @property
    def right_float(self) -> float:
        return self._right_float

    @property
    def are_integer(self) -> bool:
        return self._are_valid and not self.are_float

    @property
    def left_int(self) -> int:
        return self._left_int

    @property
    def right_int(self) -> int:
        return self._right_int


def eval_expr(env: EnvTable, expr: Expr) -> Union[Expr, None]:
    if isinstance(expr, AssignmentExpr):
        result = eval_expr(env, expr.rhs)
        if result is None:
            return None
        ident_sym = expr.ident
        item_name = ident_sym.as_str("_")
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
    elif isinstance(expr, FunctionDefExpr):
        name_sym = expr.name
        item_name = name_sym.as_str("_")
        item = EnvItem(item_name, expr)
        env.set_item(item)
        return expr  # nil_expr
    elif isinstance(expr, IdentifierExpr):
        name_sym = expr.name
        item_name = name_sym.as_str("_")
        maybe_item = env.get_item(item_name)
        if maybe_item is None:
            return None
        return maybe_item.value
    elif isinstance(expr, BinaryExpr):
        return eval_binary_expr(env, expr)
    else:
        print("Another expr named: %s" % type(expr))
        return None
    return None


def add_exprs(lhs: BaseExpr, rhs: BaseExpr) -> Union[Expr, None]:
    operands = NumericOperands(lhs, rhs)
    if not operands.are_valid:
        print("Incompatible operands: %s and %s" % (lhs, rhs))
        return None

    if operands.are_integer:
        int_result = operands.left_int + operands.right_int
        print("Add values: %d + %d" % (operands.left_int, operands.right_int))
        return IntegerExpr(symtoken_for_numeric(int_result))
    elif operands.are_float:
        float_result = operands.left_float + operands.right_float
        print("Add values: %g + %g" % (operands.left_float, operands.right_float))
        return FloatExpr(symtoken_for_numeric(float_result))
    else:
        print("Operands not supported: %s and %s" % (lhs, rhs))
        return None


def multiply_exprs(lhs: BaseExpr, rhs: BaseExpr) -> Union[Expr, None]:
    operands = NumericOperands(lhs, rhs)
    if not operands.are_valid:
        print("Incompatible operands: %s and %s" % (lhs, rhs))
        return None

    if operands.are_integer:
        int_result = operands.left_int * operands.right_int
        print("Multiply values: %d * %d" % (operands.left_int, operands.right_int))
        return IntegerExpr(symtoken_for_numeric(int_result))
    elif operands.are_float:
        float_result = operands.left_float * operands.right_float
        print("Multiply values: %g * %g" % (operands.left_float, operands.right_float))
        return FloatExpr(symtoken_for_numeric(float_result))
    else:
        print("Operands not supported: %s and %s" % (lhs, rhs))
        return None


def eval_binary_expr(env: EnvTable, expr: BinaryExpr) -> Union[Expr, None]:
    operator = expr.operator
    opsym = operator.symtype
    maybe_lhs = eval_expr(env, expr.lhs)
    if maybe_lhs is None:
        return None
    maybe_rhs = eval_expr(env, expr.rhs)
    if maybe_rhs is None:
        return None
    lhs = cast(BaseExpr, maybe_lhs)
    rhs = cast(BaseExpr, maybe_rhs)

    if opsym == SymbolType.OP_ADD:
        return add_exprs(lhs, rhs)

    elif opsym == SymbolType.OP_MULTIPLY:
        return multiply_exprs(lhs, rhs)

    else:
        print("Unexpected operator: %s" % opsym.name)
        return None


def eval_other(env: EnvTable, stmt: Stmt) -> None:
    stmt_line = 0
    print("Evaluating [%2d] %s" % (stmt_line, stmt))
    return None


def eval_stmt(env: EnvTable, stmt: Stmt) -> Union[Expr, None]:
    if isinstance(stmt, ExpressionStmt):
        return eval_expr(env, stmt.expression)
    else:
        eval_other(env, stmt)
        return None
