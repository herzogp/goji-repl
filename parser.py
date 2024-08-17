from tokenizer import (
    tokenize_program,
)

from atom import (
    AtomType,
    NodeType,
    NodeItem,
)

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
                self._type = AtomType.BOOL
            if self._val == '#f':
                self._val = False
                self._type = AtomType.BOOL
        return self

    def isident(self):
        return self._typ == AtomType.IDENT

    # Equivalent method for EnvItem
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

    def isbool(self):
        return False

    def get_value(self):
        return self._val

    def __str__(self):
        return "Atom-%s(%s)" % (self._typ.name, self._val)


# tk is a TokenItem
def parse_atom(tk_item):
    tk_type = tk_item.t
    tk_str = tk_item.value()
    if tk_item.has_value():
        atom = Atom(tk_item)
        node = NodeItem(NodeType.ATOM)
        node.add(atom) # should add a TEXT/INT/FLOAT/IDENT item here
        return node
    else:
        return None

# return None if no adjustment is warranted
# Otherwise, returns the adjusted node, and the number of additional tokens consummed
def adjusted_node(maybe_node, more_tokens):
    the_atom = maybe_node.get_value()
    the_atom_val = the_atom.get_value()
    print('the_atom: ' + str(the_atom))
    if the_atom.issymbol() and (the_atom_val == '#') and (len(more_tokens) > 1):
        print('seeing a #')
        the_next_tk = more_tokens[1]
        the_next_node = parse_atom(the_next_tk)
        print('next_node: ' + str(the_next_node))
        did_apply = False
        if the_next_node != None:
            if the_next_node.did_apply_symbol(the_atom_val):
                print('Did apply to something...\n')
                return the_next_node, 1
    print('Did not apply it\n')
    return None

def parse_list(tokens):
    nx = len(tokens)
    if nx == 0:
        return None
    node = NodeItem(NodeType.LIST) # should be more like NodeType.EXPR
    idx = 0
    tk = tokens[idx]
    # tk_type = tk.t
    while not tk.is_list_end():
        # One of: [IDENT, INTEGER, FLOAT, TEXT, BOOL]
        if tk.has_value(): 
            new_node = parse_atom(tk)
            if new_node != None:
                # (was) node.add(new_node)
                adjusted_result = adjusted_node(new_node, tokens[idx:])
                if adjusted_result != None:
                    new_node, num_tokens_used = adjusted_result
                    idx = idx + num_tokens_used
                node.add(new_node)

        # One of: [LPAREN]
        #elif tk.islist():
        elif tk.is_list_begin():
            maybe_list = parse_list(tokens[idx:])
            if maybe_list == None:
                print("Unexpected end of sub-list")
                return None
            sub_list, rest_tokens = maybe_list
            node.add(sub_list)
            idx = idx + len(sub_list) + 1
        #...

        idx = idx + 1
        if idx >= len(tokens):
            print("Unexpected end of list")
            return None
        tk = tokens[idx]
        # tk_type = tk.t

    return node, tokens[idx+1:] # should be number of tokens consummed, not [1:]

# tokens is an array of TokenItem
def parse_node(tokens):
    if len(tokens) == 0:
        return None

    # See if this is an ATOM
    tk = tokens[0]
    maybe_node = parse_atom(tk)
    if maybe_node != None:
        # return maybe_node, tokens[1:]
        adjusted_result = adjusted_node(maybe_node, tokens)
        new_idx = 1
        if adjusted_result != None:
            maybe_node, num_tokens_used = adjusted_result
            new_idx = new_idx + num_tokens_used
        return maybe_node, tokens[new_idx:]

    # Must be a LIST - better check anyway
    # elif tk.islist():
    elif tk.is_list_begin():
        # either returns None
        # or (node, [more_tokens])
        return parse_list(tokens[1:])
    else:
        print('Unexpected: ', str(tk))
        return None

def parse_program(file_path):
    tokens = tokenize_program(file_path)
    tk_count = len(tokens)
    if tk_count > 0:
        print('%i tokens found in "%s"' % (tk_count, file_path))

    all_nodes = []
    parsed_result = parse_node(tokens)
    while parsed_result != None:
        node, tokens = parsed_result
        all_nodes.append(node)
        parsed_result = parse_node(tokens)
    return all_nodes
