import itertools
from enum import Enum

from env import (
    EnvItem,
)

from atom import (
    Builtin,
)

from intrinsics import (
    define_item,
    num_args_for_op,
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
    # should be a version builtin that returns this text
    # engine_id = environment.get_integer('engineVersion-id')
    # engine_name = environment.get_text('engineVersion-name')[0]
    # print(f"engineVersion: {engine_name}({engine_id})\n")
    sub_item = atom.get_value()
    if sub_item.isident():
       env_name = sub_item.get_value()

       x = environment.get_item(env_name)

       # TODO: Why return the ident here? 
       # Because it must be a define???? 
       if x == None:
            return sub_item

       # x is an EnvItem with .name .typ and .value properties
       if uses_atoms:
           xval = x.value
           return xval
    return sub_item

def eval_node(environment, node):
    if node.isatom():
        return eval_atom(environment, node)
    else:
        operator = eval_node(environment, node.get_item(0)).get_value()
        print("Operator: ", operator)
        print("OP: '%s' '%s' %s" % (str(operator), node.get_item(0)._typ, type(operator)))
        if operator in Builtin:
            nargs = len(node) - 1
            op_name, args_expected = num_args_for_op(operator)
            if nargs < args_expected:
                suffix = "s"
                if nargs == 1:
                    suffix = ""
                print("Unable to evaluate '%s' - needs more than %d argument%s" % (op_name, nargs, suffix))
                return 0
            if operator in Builtin:
                all_args = [node.get_item(1+idx) for idx in range(args_expected)]
                return apply_op(environment, operator, all_args)

        else:
            print("Expected an operator, found '%s'" % str(operator))
    
        return 0

def apply_op(environment, op, all_args):
    if op == Builtin.DEFINE:
        # The name of the item to define
        name_node = all_args[0]
        if not name_node.isatom():
            print("Unable to assign a value to ", name_atom)    
            return 0
        name_atom = name_node.get_value()
        if not name_atom.isident():
            print("Unable to assign a value to ", name_atom)    
            return 0
        item_name = name_atom.get_value()

        # The value to be defined
        val_atom = eval_node(environment, all_args[1]) # should return a NewAtom-INTEGER(17), not an EnvItem
        print("define(%s, %s)" % (item_name, val_atom.get_value()))
        return define_item(environment, item_name, val_atom)
    elif op == Builtin.OP_ADD:
        left_operand = eval_node(environment, all_args[0])
        right_operand = eval_node(environment, all_args[1])
        left_val = left_operand.get_value()
        right_val = right_operand.get_value()
        result = left_val + right_val
        print("ADD(%d, %d)" % (left_val, right_val))
        # print("==> %d" % result)
        new_atom = Atom(TokenItem(Token.NUMERIC,str(result)))
        return new_atom
    elif op == Builtin.OP_MULT:
        left_operand = eval_node(environment, all_args[0])
        right_operand = eval_node(environment, all_args[1])
        left_val = left_operand.get_value()
        right_val = right_operand.get_value()
        result = left_val * right_val
        print("MULT(%d, %d)" % (left_val, right_val))
        # print("==> %d" % result)
        new_atom = Atom(TokenItem(Token.NUMERIC, str(result)))
        return new_atom
