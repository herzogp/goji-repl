import itertools
from enum import Enum

class ItemType(Enum):
    INTEGER = 1
    FLOAT = 2
    TEXT = 3
    BOOL = 4
    LIST = 5
    FUNCTION = 6
    NIL = 7

class EnvItem:
    def __init__(self, name, typ, value=tuple()):
        if typ == ItemType.NIL:
            if name != "nil" or value != tuple():
                raise Exception("Cannot create nil value")
        self._name = name
        self._typ = typ
        if value == tuple():
            print("value is equal to tuple()")
            if typ == ItemType.TEXT:
                value = ("",)
            elif typ == ItemType.INTEGER:
                value = (0,)
            elif typ == ItemType.FLOAT:
                value = (0.0,)
            elif typ == ItemType.BOOL:
                value = (False,)
            elif typ == ItemType.LIST:
                value = ()
            # FUNCTION's should never have an empty value
            # Force this to be an empty list instead
            elif typ == ItemType.FUNCTION:
                self._typ = ItemType.LIST
                value = ()
        self._value = value
        print("created EnvItem '%s' with typ '%s' and value: " % (self._name, self._typ.name), self._value, " => type: ",  type(value))

    #ItemType.FUNCTION should include the code to be evaluated,
    # and for special forms, might be 'builtin' code
    # This might be represented as (FunctionType.NATIVE, native_code_id) or (FunctionType.USER, Params, Expr )
    #
    # Probably want to create an EnvItem from a name and an Atom
    @property
    def name(self):
        return self._name

    # Could provide an equivalent get_type() method from Atom
    @property
    def typ(self):
        return self._typ

    # Equivalent get_value() method from Atom
    @property
    def value(self):
        return self._value

    # Equivalent method for Atom
    def istext(self):
        return self._typ == ItemType.TEXT

    # Equivalent method for Atom
    def isinteger(self):
        return self._typ == ItemType.INTEGER

    # Equivalent method for Atom
    def isfloat(self):
        return self._typ == ItemType.FLOAT

    # Equivalent method for Atom
    def isbool(self):
        return self._typ == ItemType.BOOL

    # Not supported by Atom
    def isfunction(self):
        return self._typ == ItemType.FUNCTION

    # Not supported by Atom
    def islist(self):
        return self._typ == ItemType.LIST

    def clone(self):
        new_item = EnvItem(self.name, self.typ, self.value)
        return new_item

    # Equivalent method isnil() for Atom
    def isNil(self):
        if self._typ == ItemType.NIL:
            return True
        return self._name == 'nil'

    @property
    def value_repr(self):
        if self.typ == ItemType.NIL:
            return nil
        if self.typ == ItemType.LIST:
            return str(self._value)

        this_val = self._value[0]
        format_str = '%s'
        if self._typ == ItemType.TEXT:
            format_str = "'%s'"
        elif self._typ == ItemType.INTEGER:
            format_str = '%d'
        elif self._typ == ItemType.FLOAT:
            format_str = '%g'
        elif self._typ == ItemType.BOOL:
            format_str = '%s'
        elif self._typ == ItemType.FUNCTION:
            return "%s(%d)" % (this_val.name, this_val.value)
        else:
            format_str = '?%s'
        return format_str % this_val

    def __str__(self):
        if self.typ == ItemType.NIL:
            return 'nil'
        return '%s: %s' % (self.name, self.value_repr)
nil = EnvItem('nil', ItemType.NIL)


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
        if item.isNil():
            return
        new_item = item.clone()
        for idx, old_item in enumerate(self.table):
            if old_item.name == new_item.name:
                self.table[idx] = new_item
                return
        self.table.append(new_item)
        
    def get_item(self, item_name):
        if item_name == 'nil':
            return nil
        for old_item in self.table:
            if old_item.name == item_name:
                return old_item.clone()
            # else:
            #     print('Looking for "%s" [0]- it is not equal to "%s"' % (item_name, old_item.name))
        if self.parent != None:
            return self.parent.get_item(item_name)
        else:
            return None

    def get_integer(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.isinteger():
            return env_item.value[0]
        return 0

    def get_text(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.istext():
            return env_item.value
        return "" 

    def get_bool(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.isbool():
            return env_item.value[0]
        return False

    def show(self):
        for item in self.table:
            print(str(item))

# ----------------------------------------------------------------------
# NOTE:
# parse into a list of EXPR's
# then, evaluate these EXPRS's from top to bottom
# EXPR is () which evaluates to '()'
# or TEXT which evaluates to 'TEXT'
# or NUMBER which evaluates to NUMBER
# or IDENT which evaluates to LOOKUP(ENV, IDENT) where ENV includes builtins
# or (IDENT,'def')
# or (EXPR arg1 arg2 ...) which evaluates to:
#   let fn = LOOKUP(ENV, EXPR)
#   let new_env = COPY(ENV)
#   for param,idx in fn.PARAM_NAMES
#       let arg = arglist[idx]
#       let argval = EVAL(ENV, arg)
#       SET(new_env, param, argval)
#   EVAL(new_env, fn.BODY)
# ----------------------------------------------------------------------


# nam is a primitive/native TEXT
# atom must support isinteger(), isfloat(), istext(), isbool() and get_value()
# Both NewAtom and OldAtom support these methods
def define_item(environment, nam, atom):
    if atom.isinteger():
        int_item = EnvItem(nam, ItemType.INTEGER, (atom.get_value(),))
        environment.set_item(int_item)
    if atom.isfloat():
        float_item = EnvItem(nam, ItemType.FLOAT, (atom.get_value(),))
        environment.set_item(float_item)
    if atom.istext():
        text_item = EnvItem(nam, ItemType.TEXT, (atom.get_value(),))
        environment.set_item(text_item)
    if atom.isbool():
        bool_item = EnvItem(nam, ItemType.BOOL, (atom.get_value(),))
        environment.set_item(bool_item)
    return atom

