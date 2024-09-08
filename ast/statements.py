from ast.interfaces import Expr

class BlockStmt:
    def __init__(self, stmts):
        self._stmts = stmts

class ExpressionStmt:
    def __init__(self, expression):
        self._expression = expression

    def __str__(self):
        return str(self._expression)

    @property
    def expression(self):
        return self._expression

    @property
    def line(self):
        return self._expression.line
