from ast.interfaces import Expr

from parser.symbols import SymToken 

class BaseExpr:
    def __init__(self, sym):
        self._sym = sym
        # TODO:
        # if not isinstance(sym, SymToken):
        #     raise Exception("Only SymTokens can be BaseExpr's")

    @property
    def symbol(self):
        return self._sym

    @property
    def line(self):
        return self._sym.line

    @property
    def col(self):
        return self._left.col
        
    @property
    def exprvalue(self):
        return self._sym.symvalue

    @property
    def exprtype(self):
        return self._sym.symtype

class IntegerExpr(BaseExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "IntegerLiteral(%d)" % self.exprvalue

class FloatExpr(BaseExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "FloatLiteral(%g)" % self.exprvalue

class BoolExpr(BaseExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "BoolLiteral(%b)" % self.exprvalue

class StringExpr(BaseExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "StringLiteral('%s')" % self.exprvalue

class IdentifierExpr:
    def __init__(self, ident):
        self._ident = ident

    @property
    def ident(self):
        return self._ident

    def __str__(self):
        return "Identifier(%s)" % self._ident


class AssignmentExpr:
    def __init__(self, ident, rhs):
        self._ident = ident
        self._rhs = rhs

    def __str__(self):
        return "AssignmentExpr(IDENT: %s, Value: %s)" % (self._ident, self._rhs)

    @property
    def rhs(self):
        return self._rhs

    @property
    def ident(self):
        return self._ident


class BinaryExpr:
    def __init__(self, op, lhs, rhs):
        self._op = op
        self._lhs = lhs
        self._rhs = rhs

    def __str__(self):
        return "BinaryExpr(OP:'%s', Left: %s, Right: %s)" % (self._op.symvalue, self._lhs, self._rhs)

    @property
    def operator(self):
        return self._op

    @property
    def lhs(self):
        return self._lhs

    @property
    def rhs(self):
        return self._rhs
