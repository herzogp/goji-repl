from typing import Union, Any, cast

from ast.interfaces import Expr

from ast.expressions import (
    BaseExpr,
    NilExpr,
)

from parser.symbols import (
    nil_symtoken,
)

# EnvItem is a name + BaseExpr
class EnvItem:
    def __init__(self, name: str, expr: Expr) -> None:
        self._name = name
        self._expr = expr


    @property
    def name(self) -> str:
        return self._name

    @property
    def value(self) -> Expr:
        return self._expr

    @property
    def old_value(self) -> Any:
        if not isinstance(self._expr, BaseExpr):
            return None
        return self._expr.exprvalue

    def isstring(self) -> bool:
        if not isinstance(self._expr, BaseExpr):
            return False
        item_sym = self._expr.exprsym
        return item_sym.isstring()

    def isinteger(self) -> bool:
        if not isinstance(self._expr, BaseExpr):
            return False
        item_sym = self._expr.exprsym
        return item_sym.isinteger()

    def isfloat(self) -> bool:
        if not isinstance(self._expr, BaseExpr):
            return False
        item_sym = self._expr.exprsym
        return item_sym.isfloat()

    def isbool(self) -> bool:
        if not isinstance(self._expr, BaseExpr):
            return False
        item_sym = self._expr.exprsym
        return item_sym.isbool()

    def isfunction(self) -> bool:
        return False

    def clone(self) -> EnvItem:
        new_item = EnvItem(self._name, self._expr)
        return new_item

    # Equivalent method isnil() for Atom
    def isnil(self) -> bool:
        if not isinstance(self._expr, BaseExpr):
            return False
        item_sym = self._expr.exprsym
        return item_sym.isnil()

    def __str__(self) -> str:
        if self.isnil():
            return 'nil'
        return '%s: %s' % (self._name, self._expr)

nil_expr = NilExpr(nil_symtoken)
nil = EnvItem('nil', nil_expr)

class EnvTable:
    def __init__(self, parent_env: Union[EnvTable, None] = None) -> None:
        self.parent = parent_env
        self.table: list[EnvItem] = [] # could be a HashMap soon
        # if not self.parent is None:
        #     self.version = self.parent.version

    @property
    def size(self) -> int:
        return len(self.table)

    def set_item(self, item: EnvItem) -> None:
        if item.isnil():
            return
        # caller is trusted to not modify
        # the item - they relinquish write access
        # otherwise, the item should be cloned
        # new_item = item.clone()
        new_item = item
        for idx, old_item in enumerate(self.table):
            if old_item.name == new_item.name:
                print("Replacing %s with %s" % (new_item.name, new_item))
                self.table[idx] = new_item
                return
        print("Creating item: %s" % new_item)
        self.table.append(new_item)

    def hasTopLevelValue(self, item_name: str) -> bool:
        if item_name == 'nil':
            return True
        for old_item in self.table:
            if old_item.name == item_name:
                return True
        return False

    def get_item(self, item_name: str) -> Union[EnvItem, None]:
        if item_name == 'nil':
            return nil
        for old_item in self.table:
            if old_item.name == item_name:
                # trust the caller
                return old_item
                # return old_item.clone if the caller is untrusted
        if self.parent is None:
            return None
        return self.parent.get_item(item_name)

    def get_integer(self, item_name: str) -> int:
        env_item = self.get_item(item_name)
        if env_item is None:
            return 0
        if env_item.isinteger():
            return cast(int, env_item.value)
        return 0

    def get_float(self, item_name: str) -> float:
        env_item = self.get_item(item_name)
        if env_item is None:
            return 0.0
        if env_item.isfloat():
            return cast(float, env_item.value)
        return 0.0

    def get_bool(self, item_name: str) -> bool:
        env_item = self.get_item(item_name)
        if env_item is None:
            return False
        if env_item.isbool():
            return cast(bool, env_item.value)
        return False

    def get_text(self, item_name: str) -> str:
        env_item = self.get_item(item_name)
        if env_item is None:
            return "" 
        if env_item.isstring():
            return cast(str, env_item.value)
        return "" 

    def show(self) -> None:
        for item in self.table:
            print(str(item))
