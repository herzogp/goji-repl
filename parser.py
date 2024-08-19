from tokenizer import (
    tokenize_program,
    Token, 
    TokenItem,
)

from atom import (
    AtomType,
    Atom,
)

from node import (
    NodeType,
    Node,
)


# parse_atom: TokenItem -> Node
def parse_atom(tk_item):
    tk_type = tk_item.t
    tk_str = tk_item.value()
    if tk_item.has_value():
        atom = Atom(tk_item)
        node = Node(NodeType.ATOM)
        node.add(atom) # should add a TEXT/INT/FLOAT/IDENT item here
        return node
    else:
        return None

# return None if no adjustment is warranted
# Otherwise, returns the adjusted node, and the number of additional tokens consummed
def adjusted_node(maybe_node, more_tokens):
    the_atom = maybe_node.get_value()
    the_atom_val = the_atom.get_value()
    if the_atom.issymbol():
        if (the_atom_val == '#') and (len(more_tokens) > 1):
            the_next_tk = more_tokens[1]
            the_next_node = parse_atom(the_next_tk)
            did_apply = False
            if the_next_node != None:
                if the_next_node.did_apply_symbol(the_atom_val):
                    return the_next_node, 1
        elif the_atom_val == '+':
            new_atom = Atom(TokenItem(Token.QTEXT, '#add')).asbuiltin()
            new_node = Node(NodeType.ATOM)
            new_node.add(new_atom)
            return new_node, 0
    return None

# parse_list: Stream<TokenItem> -> Node
def parse_list(tokens):
    nx = len(tokens)
    if nx == 0:
        return None
    node = Node(NodeType.LIST) # should be more like NodeType.EXPR
    idx = 0
    tk = tokens[idx]
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

# parse_node: Stream<TokenItem> -> Node
def parse_node(tokens):
    if len(tokens) == 0:
        return None

    # See if this is an ATOM
    tk = tokens[0]
    maybe_node = parse_atom(tk)
    if maybe_node != None:
        adjusted_result = adjusted_node(maybe_node, tokens)
        new_idx = 1
        if adjusted_result != None:
            maybe_node, num_tokens_used = adjusted_result
            new_idx = new_idx + num_tokens_used
        return maybe_node, tokens[new_idx:]

    # Must be a LIST - better check anyway
    elif tk.is_list_begin():
        # either returns None
        # or (node, [more_tokens])
        return parse_list(tokens[1:])
    else:
        print('Unexpected: ', str(tk))
        return None

# parse_program: FilePath -> Node[]
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
