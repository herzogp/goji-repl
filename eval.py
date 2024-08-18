import itertools
from enum import Enum

from env import (
    EnvItem,
    ItemType,
    define_item,
)

from atom import (
    Builtin,
)

from parser import (
    Atom,
)

from tokenizer import (
    Token,
    TokenItem,
    tokenize_program,
)

def env_item_to_atom(env_item):
    if env_item.isinteger():
        return Atom(TokenItem(Token.NUMERIC, str(env_item.value[0])))
    elif env_item.isfloat():
        return Atom(TokenItem(Token.NUMERIC, str(env_item.value[0])))
    elif env_item.istext():
        return Atom(TokenItem(Token.TEXT, env_item.value[0]))
    elif env_item.isbool():
        if env_item.value[0]:
            this_atom = Atom(TokenItem(Token.TEXT, '#t'))
            return this_atom.asbool()
        else:
            this_atom = Atom(TokenItem(Token.TEXT, '#f'))
            return this_atom.asbool()
    # not sure how to do this yet
    # elif env_item.isfunction():
    #     return TokenItem(Token.BUILTIN, env_item.value[0])
    else:
        return Atom(TokenItem(Token.LIST_BEGIN, ''))

# ATOM values are not the same as primitive values
# e.g. ATOM(BOOL, 't') is not the same as True
# and ATOM(INTEGER, 19) is not the same as 19
#
# Returns Native values: int, float, str, bool 
# which are stored in class NewAtom
def eval_atom(environment, atom):
    uses_atoms = environment.get_integer('engineVersion-id') >= 0
    engine_id = environment.get_integer('engineVersion-id')
    engine_name = environment.get_text('engineVersion-name')[0]
    print(f"engineVersion: {engine_name}({engine_id})\n")
    #print("engineVersion: %s\n" % engine_name)
    sub_item = atom.get_value()
    if sub_item.isident():
       env_name = sub_item.get_value()
       print("eval_atom: Should lookup '%s' in the environment" % env_name)

       x = environment.get_item(env_name)

       # TODO: Why return the ident here? 
       # Because it must be a define???? 
       if x == None:
            print("eval_atom: lookup failed returning atom.get_value() => ", str(sub_item))
            return sub_item

       # x is an EnvItem with .name .typ and .value properties
       print(type(x))
       print("X is: ", x, "  its type is: ", type(x))
       if uses_atoms:
           print("eval_atom: uses_atoms x: ", type(x), str(x))
           xval = x.value
           return xval
           # [PH] print("eval_atom(env, '%s') returns %s with type: " % (env_name, xval),type(xval), "not using x.typ")
           # [PH] if x.isfunction():
           # [PH] #if x.typ == ItemType.FUNCTION:
           # [PH]      return xval[0]
           # [PH] return env_item_to_atom(x)
    return sub_item

def eval_node(environment, node):
    if node.isatom():
        return eval_atom(environment, node)
    else:
        print("this node(not an atom): ", node)
        firstNodeItem = node.get_item(0)
        print("firstNodeItem: ", firstNodeItem)
        operator = eval_node(environment, node.get_item(0)).get_value()
        print("OP: " + str(operator), type(operator))
        if operator in Builtin:
            print("Operator is some sort of builtin: ", operator.name)
            if operator == Builtin.DEFINE:
                print("hard-coded DEFINE goes here")
                name_atom = eval_node(environment, node.get_item(1))
                if name_atom.isident():
                    tk_item = name_atom.get_value()
                    item_name = tk_item #._val
                    print("Making recursive call to eval_node with ", node.get_item(2), node.get_item(1), node.get_item(0))
                    val_atom = eval_node(environment, node.get_item(2)) # should return a NewAtom-INTEGER(17), not an EnvItem
                    print("eval_node[306] op is a Builtin: val_atom: " + str(val_atom) + ' ', type(val_atom))
                    print("define(%s, %s)" % (item_name, val_atom.get_value()))
                    return define_item(environment, item_name, val_atom)
        else:
            print("Expected an operator, found '%s'" % str(operator))
    
        return 0

def eval_ident(environment, ident):
    # lookup the ident._val in the environment
    # for the 'define' builtin', this lookup should return
    # an indication that this is a builtin, and the specific
    # builtin identifier
    pass
