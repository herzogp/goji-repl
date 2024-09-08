from ast.expressions import (
    BaseExpr,
    NilExpr,
)

from parser.symbols import (
    nil_symtoken,
)

# EnvItem is a name + BaseExpr
class EnvItem:
    def __init__(self, name, expr):
        self._name = name
        self._expr = expr


    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._expr.exprvalue

    def isstring(self):
        item_sym = self._expr.exprsym
        return item_sym.isstring()

    def isinteger(self):
        item_sym = self._expr.exprsym
        return item_sym.isinteger()

    def isfloat(self):
        item_sym = self._expr.exprsym
        return item_sym.isfloat()

    def isbool(self):
        item_sym = self._expr.exprsym
        return item_sym.isbool()

    def isfunction(self):
        pass

    def clone(self):
        new_item = EnvItem(self._name, self._expr)
        return new_item

    # Equivalent method isnil() for Atom
    def isnil(self):
        item_sym = self._expr.exprsym
        return item_sym.isnil()

    @property
    def value_repr(self):
        if self.isnil():
            return 'nil'
        # elif self.islist():
        #     return str(self.value)
        else:
            return str(self.value)

    def __str__(self):
        if self.isnil():
            return 'nil'
        return '%s: %s' % (self.name, self.value_repr)

nil_expr = NilExpr(nil_symtoken)
nil = EnvItem('nil', nil_expr)

class EnvTable:
    def __init__(self, parent_env=None):
        self.parent = parent_env
        self.table = [] # could be a HashMap soon
        if self.parent != None:
            self.version = self.parent.version

    @property
    def size(self):
        return len(self.table)

    def set_item(self, item):
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

    def hasTopLevelValue(self, item_name):
        if item_name == 'nil':
            return True
        for old_item in self.table:
            if old_item.name == item_name:
                return True
        return False

    def get_item(self, item_name):
        if item_name == 'nil':
            return nil
        for old_item in self.table:
            if old_item.name == item_name:
                # trust the caller
                return old_item
                # return old_item.clone if the caller is untrusted
        if self.parent != None:
            return self.parent.get_item(item_name)
        else:
            return None

    def get_integer(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.isinteger():
            return env_item.value
        return 0

    def get_float(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.isfloat():
            return env_item.value
        return 0.0

    def get_bool(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.isbool():
            return env_item.value
        return False

    def get_text(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.isstring():
            return env_item.value
        return "" 

    def show(self):
        for item in self.table:
            print(str(item))
