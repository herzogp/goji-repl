from ast.interfaces import Expr

class IntegerExpr:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "IntegerLiteral(%d)" % self._value

class FloatExpr:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "FloatLiteral(%g)" % self._value

class BoolExpr:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "BoolLiteral(%b)" % self._value

class StringExpr:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "StringLiteral('%s')" % self._value

class IdentifierExpr:
    def __init__(self, value):
        self._value = value

    def __str__(self):
        return "Identifier(%s)" % self._value

class BinaryExpr:
    def __init__(self, op, left, right):
        self._op = op
        self._left = left
        self._right = right

    def __str__(self):
        return "BinaryExpr(OP: %s, Left: %s, Right: %s)" % (self._op, self._left, self._right)
