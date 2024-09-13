from typing import Union

from ast.interfaces import Expr, Stmt

from parser.symbols import SymToken, SymbolType

class BaseExpr(Expr):
    def __init__(self, sym: SymToken) -> None:
        self._sym = sym
        # TODO:
        # if not isinstance(sym, SymToken):
        #     raise Exception("Only SymTokens can be BaseExpr's")

    @property
    def line(self) -> int:
        return self._sym.line

    @property
    def col(self) -> int:
        return self._sym.col
        
    @property
    def exprvalue(self) -> Union[int, float, str, bool]:
        return self._sym.symvalue

    @property
    def exprtype(self) -> SymbolType:
        return self._sym.symtype

    @property
    def exprsym(self) -> SymToken:
        return self._sym

    def expr(self) -> None:
        return None

class NilExpr(BaseExpr):
    def __init__(self, sym: SymToken) -> None:
        super().__init__(sym)

    def __str__(self) -> str:
        return "NilLiteral"

class IntegerExpr(BaseExpr):
    def __init__(self, sym: SymToken) -> None:
        super().__init__(sym)

    def __str__(self) -> str:
        return "IntegerLiteral(%d)" % int(self.exprvalue)

class FloatExpr(BaseExpr):
    def __init__(self, sym: SymToken) -> None:
        super().__init__(sym)

    def __str__(self) -> str:
        return "FloatLiteral(%g)" % float(self.exprvalue)

class BoolExpr(BaseExpr):
    def __init__(self, sym: SymToken) -> None:
        super().__init__(sym)

    def __str__(self) -> str:
        return "BoolLiteral(%s)" % self.exprvalue

class StringExpr(BaseExpr):
    def __init__(self, sym: SymToken) -> None:
        super().__init__(sym)

    def __str__(self) -> str:
        return "StringLiteral('%s')" % self.exprvalue

class IdentifierExpr(Expr):
    def __init__(self, sym: SymToken) -> None:
        self._sym = sym

    @property
    def name(self) -> SymToken:
        return self._sym

    def __str__(self) -> str:
        return "Identifier(%s)" % self._sym

    @property
    def line(self) -> int:
        return self._sym.line

    def expr(self) -> None:
        return None

class AssignmentExpr(Expr):
    def __init__(self, ident: SymToken, rhs: Expr):
        self._ident = ident
        self._rhs = rhs

    def __str__(self) -> str:
        return "AssignmentExpr(IDENT: %s, Value: %s)" % (self._ident, self._rhs)

    @property
    def rhs(self) -> Expr:
        return self._rhs

    @property
    def ident(self) -> SymToken:
        return self._ident

    @property
    def line(self) -> int:
        return self._ident.line

    def expr(self) -> None:
        return None

class ParamsExpr(Expr):
    def __init__(self, params: list[IdentifierExpr]) -> None:
        super().__init__()
        self._params = params

    @property
    def params(self) -> list[IdentifierExpr]:
        return self._params

    def __str__(self) -> str:
        all_params = [str(x) for x in self._params]
        str_params = ", ".join(all_params)
        return "ParamsExpr(%s)" % str_params

    def expr(self) -> None:
        return None

class FunctionExpr(IdentifierExpr):
    def __init__(self, sym: SymToken, params: ParamsExpr, body: Stmt) -> None:
        super().__init__(sym)
        self._params = params
        self._body = body

    @property
    def params(self) -> list[IdentifierExpr]:
        return self._params

    @property
    def body(self) -> Stmt:
        return self._body

    def str(self) -> str:
        all_params = [str(x) for x in self._params]
        str_params = ", ".join(all_params)
        return "FunctionExpr(%s %s)" % (self.name, str_params)

    def expr(self) -> None:
        return None

class BinaryExpr(Expr):
    def __init__(self, op: SymToken, lhs: Expr, rhs: Expr):
        self._op = op
        self._lhs = lhs
        self._rhs = rhs

    def __str__(self):
        return "BinaryExpr(OP:'%s', Left: %s, Right: %s)" % (self._op.symvalue, self._lhs, self._rhs)

    @property
    def operator(self) -> SymToken:
        return self._op

    @property
    def lhs(self)-> Expr:
        return self._lhs

    @property
    def rhs(self) -> Expr:
        return self._rhs

    @property
    def line(self) -> int:
        return self._op.line

    def expr(self) -> None:
        return None
