from ast.interfaces import Expr

from parser.symbols import SymToken 

class SourceExpr:
    def __init__(self, sym):
        self._sym = sym
        # if not isinstance(sym, SymToken):
        #     raise Exception("Only SymTokens can be SourceExpr's")

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
    def value(self):
        return self._sym.symvalue

class IntegerExpr(SourceExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "IntegerLiteral(%d)" % self.value

class FloatExpr(SourceExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "FloatLiteral(%g)" % self.value

class BoolExpr(SourceExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "BoolLiteral(%b)" % self.value

class StringExpr(SourceExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "StringLiteral('%s')" % self.value

class IdentifierExpr(SourceExpr):
    def __init__(self, sym):
        super().__init__(sym)

    def __str__(self):
        return "Identifier(%s)" % super().value


class AssignmentExpr(SourceExpr):
    def __init__(self, ident, rhs):
        super().__init__(ident)
        self._rhs = rhs

    def __str__(self):
        return "AssignmentExpr(IDENT: %s, Value: %s)" % (self.symbol, self._rhs)

    @property
    def rhs(self):
        return self._rhs

    @property
    def ident(self):
        return super().symbol


class BinaryExpr(SourceExpr):
    def __init__(self, op, lhs, rhs):
        super().__init__(op)
        # self._op = op
        self._lhs = lhs
        self._rhs = rhs

    def __str__(self):
        return "BinaryExpr(OP:'%s', Left: %s, Right: %s)" % (self.symbol.symvalue, self._lhs, self._rhs)
        

    @property
    def operator(self):
        return super().symbol

    @property
    def lhs(self):
        return self._lhs

    @property
    def rhs(self):
        return self._rhs
