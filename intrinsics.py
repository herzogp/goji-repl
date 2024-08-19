from enum import Enum

from node import(
    Node,
    NodeType,
)

from env import(
    EnvItem,
)

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
