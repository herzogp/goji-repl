from ast.interfaces import Expr, Stmt

class BlockStmt(Stmt):
    def __init__(self, stmts) -> None:
        self._stmts = stmts

    @property
    def line(self) -> int:
        if len(self._stmts) == 0:
            return 0
        else:
            first_stmt = self._stmts[0]
            return first_stmt.line

    def stmt(self) -> None:
        return None

    @property
    def some_name(self) -> None:
        return None

    

class ExpressionStmt(Stmt):
    def __init__(self, expression: Expr) -> None:
        super().__init__()
        self._expression = expression

    def __str__(self) -> str:
        return str(self._expression)

    @property
    def expression(self) -> Expr:
        return self._expression

    @property
    def line(self) -> int:
        return self._expression.line

    def stmt(self) -> None:
        return None

    @property
    def some_name(self) -> None:
        return None
