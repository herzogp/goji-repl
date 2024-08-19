import itertools
from enum import Enum

from node import(
    Node,
    NodeType,
    make_atom_node,
)

from atom import(
    Atom,
)

from tokenizer import(
    Token,
    TokenItem,
)

def toAtom(node):
    if node == None:
        return Atom(TokenItem(Token.UNKNOWN))

    if node.isatom():
        return node.get_value()
    return None

def toList(node):
    if node.islist():
        return node.get_value()
    return None

# EnvItem can be a name + Node
class EnvItem:
    def __init__(self, name, node):
        self._name = name
        self._node = node


    @property
    def name(self):
        return self._name

    @property
    def value(self):
        return self._node.get_value() # returns an Atom or a hierarchical list of Atoms

    def isatom(self):
        return self._node.isatom()

    def islist(self):
        return self._node.islist()

    def istext(self):
        if not self._node.isatom():
            return False
        atom = self._node.get_value()
        return atom.istext()

    def isinteger(self):
        if not self._node.isatom():
            return False
        atom = self._node.get_value()
        return atom.isinteger()

    def isfloat(self):
        if not self._node.isatom():
            return False
        atom = self._node.get_value()
        return atom.isfloat()

    def isbool(self):
        if not self._node.isatom():
            return False
        atom = self._node.get_value()
        return atom.isbool()

    def isfunction(self):
        if not self._node.isatom():
            return False
        atom = self._node.get_value()
        return atom.isfunction()

    def clone(self):
        new_item = EnvItem(self.name, self._node)
        return new_item

    # Equivalent method isnil() for Atom
    def isNil(self):
        if not self._node.isatom():
            return False
        atom = self._node.get_value()
        return atom.isnil()

    @property
    def value_repr(self):
        if self.isNil():
            return 'nil'
        elif self.islist():
            return str(self.value)
        elif self.isatom():
            return str(self.value.get_value())
        else:
            return "??<unknown>??"

    def __str__(self):
        if self.isNil():
            return 'nil'
        return '%s: %s' % (self.name, self.value_repr)

nil = EnvItem('nil', make_atom_node(Token.UNKNOWN))


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
            return env_item.value.get_value()
        return 0

    def get_text(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.istext():
            return env_item.value.get_value()
        return "" 

    def get_bool(self, item_name):
        env_item = self.get_item(item_name)
        if env_item.isbool():
            return env_item.value.get_value()
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
    does_exist = environment.hasTopLevelValue(nam)
    if does_exist:
        print("%s is immutable - should not be modifying it" % nam)
        return environment.get_item(nam)
    new_node = Node(NodeType.ATOM)
    new_node.add(atom)
    new_item = EnvItem(nam, new_node)
    environment.set_item(new_item)
    return atom

