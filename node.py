from enum import Enum

from tokenizer import(
    Token,
    TokenItem,
)

from atom import(
    Atom
)

class NodeType(Enum):
    ATOM = 1
    LIST = 2

# A Node can be either a single ATOM, 
# or a LIST (of other Nodes)
# In either case, this is called an Expression
class Node:
    def __init__(self, node_typ):
        self._typ = node_typ
        self.exprs = []
   
    # expr is either an Atom or a List
    def add(self, expr):
        self.exprs.append(expr)

    def get_value(self):
        if not self.isatom():
            all_exprs = self.exprs
            return [n.get_value() for n in all_exprs]
        return self.exprs[0]

    def get_item(self, idx):
        if idx < 0 or idx >= self.__len__():
            return None
        else:
            return self.exprs[idx]

    def isatom(self):
        return self._typ == NodeType.ATOM

    # returns an array of nodes
    def get_list(self):
        if not self.islist():
            return None
        # [Seems wrong] return self.exprs[0]
        return self.exprs

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

def make_atom_node(tk_type: Token, tk_val=''):
    node = Node(NodeType.ATOM)
    tk_item = TokenItem(tk_type, tk_val)
    node.add(Atom(tk_item))
    return node

def make_node_from_atom(atom):
    node = Node(NodeType.ATOM)
    node.add(atom)
    return node
