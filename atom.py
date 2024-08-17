from enum import Enum

class Builtin(Enum):
    DEFINE = 1
    OP_PLUS = 2
    OP_MULT = 3

class AtomType(Enum):
    TEXT = 1
    INTEGER = 2
    FLOAT = 3
    IDENT = 4
    BOOL = 5
    SYMBOL = 6
    NIL = 7

class NodeType(Enum):
    ATOM = 1
    LIST = 2

# A Node can be either a single ATOM, 
# or a LIST (of other Nodes)
# In either case, this is called an Expression
class NodeItem:
    def __init__(self, node_typ):
        self._typ = node_typ
        self.exprs = []
   
    # expr is either an Atom or a List
    def add(self, expr):
        self.exprs.append(expr)

    def get_value(self):
        if not self.isatom():
            return None
        return self.exprs[0]

    def get_item(self, idx):
        if idx < 0 or idx >= self.__len__():
            return None
        else:
            return self.exprs[idx]

    def isatom(self):
        return self._typ == NodeType.ATOM

    def get_list(self):
        if not self.islist():
            return None
        return self.exprs[0]

    def islist(self):
        return self._typ == NodeType.LIST

    def did_apply_symbol(self, s):
        if s != '#':
            return False
        atom_val = self.get_value()
        if atom_val == None:
            return False
        return self.exprs[0].did_apply_symbol(s)

    def __len__(self):
        return len(self.exprs)

    def __str__(self):
        args = ', '.join([str(item) for item in self.exprs])
        return '#%s(%s)' % (self._typ.name, args)


