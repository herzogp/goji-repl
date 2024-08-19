from enum import Enum

from atom import (
    Builtin,
)

from node import(
    Node,
    NodeType,
)

from env import(
    EnvItem,
)

def num_args_for_op(op):
    if op == Builtin.DEFINE:
        return 'define', 2
    elif op == Builtin.OP_ADD:
        return '+', 2
    elif op == Builtin.OP_MULT:
        return '*', 2
    return str(op), 0

# nam is a primitive/native TEXT
# atom must support isinteger(), isfloat(), istext(), isbool() and get_value()
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
