from abc import ABC, abstractmethod

class Stmt(ABC):
    @abstractmethod
    def stmt(self):
        pass

    @property
    @abstractmethod
    def some_name(self):
        pass

class Expr(ABC):
    @abstractmethod
    def expr(self):
        return self
