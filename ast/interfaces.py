from abc import ABC, abstractmethod

class Stmt(ABC):
    @abstractmethod
    def stmt(self) -> None:
        pass

    @property
    @abstractmethod
    def some_name(self) -> None:
        pass

class Expr(ABC):
    @abstractmethod
    def expr(self) -> None:
        pass

    @property
    def line(self) -> int:
        return 0
