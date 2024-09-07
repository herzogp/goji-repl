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
        return "Identifier(%s)" % self.value


class AssignmentExpr(SourceExpr):
    def __init__(self, ident, value):
        super().__init__(ident)
        self._value = value

    def __str__(self):
        return "AssignmentExpr(IDENT: %s, Value: %s)" % (self.symbol, self._value)

class BinaryExpr(SourceExpr):
    def __init__(self, op, left, right):
        super().__init__(op)
        # self._op = op
        self._left = left
        self._right = right

    def __str__(self):
        return "BinaryExpr(OP:'%s', Left: %s, Right: %s)" % (self.symbol.symvalue, self._left, self._right)
