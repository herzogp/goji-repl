from enum import Enum

from aug2024.old_atom import (
    Builtin,
)

from aug2024.old_node import (
    Node,
    NodeType,
)

from aug2024.old_env import (
    EnvItem,
)


def num_args_for_op(op):
    if op == Builtin.OP_ASSIGN:
        return "=", 2
    elif op == Builtin.OP_ADD:
        return "+", 2
    elif op == Builtin.OP_MULT:
        return "*", 2
    return str(op), 0


# nam is a primitive/native TEXT
# atom must support isinteger(), isfloat(), isstring(), isbool() and get_value()
def define_item(environment, nam, atom):
    does_exist = environment.has_top_level_value(nam)
    if does_exist:
        print("%s is immutable - should not be modifying it" % nam)
        return environment.get_item(nam)
    new_node = Node(NodeType.ATOM)
    new_node.add(atom)
    new_item = EnvItem(nam, new_node)
    environment.set_item(new_item)
    return atom
