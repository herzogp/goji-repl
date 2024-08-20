from enum import Enum

class Builtin(Enum):
    DEFINE = 1
    OP_ADD = 2
    OP_MULT = 3

class AtomType(Enum):
    TEXT = 1
    INTEGER = 2
    FLOAT = 3
    IDENT = 4
    BOOL = 5
    SYMBOL = 6
    NIL = 7
    # LIST = 8
    FUNCTION = 9

class Atom: # Can return AtomType.SYMBOL (but not AtomType.BOOL)
    def __init__(self, token_item):
        token_val = token_item.value()
        if token_item.is_text():
            self._typ = AtomType.IDENT
            self._val = token_val
        elif token_item.is_literal_text():
            self._typ = AtomType.TEXT
            self._val = token_val
        elif token_item.is_numeric():
            self._typ = AtomType.INTEGER # (or FLOAT)
            if token_val.find('0x') == 0:
                self._type = AtomType.INTEGER
                self._val = hex2int(token_val)
            elif (token_val.find('.') >= 0) or (token_val.find('e') > 0):
                self._typ = AtomType.FLOAT
                self._val = float(token_val)
            else:
                self._typ = AtomType.INTEGER
                self._val = int(token_val)
        elif token_item.is_symbol():
            self._typ = AtomType.SYMBOL 
            self._val = token_val
        else:
            self._typ = AtomType.NIL
            self._val = ''

    def did_apply_symbol(self, s):
        if s != '#':
            return False
        if self.isident():
            new_val = '#' + self._val
            self._val = new_val
            return True

    def asbool(self):
        if self._typ == AtomType.TEXT:
            if self._val == '#t':
                self._val = True
                self._typ = AtomType.BOOL
                return self

            if self._val == '#f':
                self._val = False
                self._typ = AtomType.BOOL
        return self

    def asbuiltin(self):
        if self._typ == AtomType.TEXT:
            if self._val == '#define':
                self._val = Builtin.DEFINE
                self._typ = AtomType.FUNCTION
            elif (self._val == '#add') or (self._val == '+'):
                self._val = Builtin.OP_ADD
                self._typ = AtomType.FUNCTION
            elif (self._val == '#mult') or (self._val == '*'):
                self._val = Builtin.OP_MULT
                self._typ = AtomType.FUNCTION
            else:
                pass
        return self

    def isfunction(self):
        return self._typ == AtomType.FUNCTION

    def isident(self):
        return self._typ == AtomType.IDENT

    def isbool(self):
        return self._typ == AtomType.BOOL

    # Equivalent method for EnvItem
    def isinteger(self):
        return self._typ == AtomType.INTEGER

    # Equivalent method for EnvItem
    def isfloat(self):
        return self._typ == AtomType.FLOAT

    # Equivalent method for EnvItem
    def istext(self):
        return self._typ == AtomType.TEXT

    def issymbol(self):
        return self._typ == AtomType.SYMBOL

    def isnil(self):
        return self._typ == AtomType.NIL

    def get_value(self):
        return self._val

    def __str__(self):
        return "Atom-%s(%s)" % (self._typ.name, self._val)

