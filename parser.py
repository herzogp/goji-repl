from tokenizer import (
    tokenize_program,
    Token, 
    TokenItem,
)

from atom import (
    AtomType,
    Atom,
    Builtin,
)

from node import (
    NodeType,
    Node,
    make_node_from_atom,
)

class Parser:
    def __init__(self):
        self._filename = ''
        self._line = 0
        self._nodes_seen = []

    @property
    def filename(self):
        return self._filename

    @filename.setter
    def filename(self, value):
        self._filename = value

    @property
    def line(self):
        return self._line

    @line.setter
    def line(self, value):
        print("Setting line to: ", value)
        self._line = value

    def has_line_numbers(self):
        return self._line > 0

    # Top of stack is end of list
    # Bottom of stack is start of list
    def push_node(self, node):
        print("  >> didPush: ", node)
        self._nodes_seen.append(node)

    def pop_node(self):
        lx = len(self._nodes_seen) - 1
        if lx < 0:
            print("pop_node() failed - returns None")
            return None
        popped_node = self._nodes_seen.pop()
        print("  << didPop: %s, new length: %d" % (popped_node, len(self._nodes_seen)))
        # return self._nodes_seen.pop()
        return popped_node

    def peek_node(self):
        lx = len(self._nodes_seen) - 1
        if lx < 0:
            return None
        return self._nodes_seen[lx]
    
    def clear_nodes(self):
        self._nodes_seen = []
    
    # parse_atom: TokenItem -> Node
    def parse_atom(self, tk_item):
        if self.has_line_numbers():
            print("[%2d] parse_atom: %s" % (self.line, tk_item))
        if tk_item.has_value():
            return make_node_from_atom(Atom(tk_item))
        else:
            return None
    
    # return None if no adjustment is warranted
    # Otherwise, returns the adjusted node
    def symbol_as_builtin(self, maybe_node):
        the_atom = maybe_node.get_value()
        the_atom_val = the_atom.get_value()
        if the_atom.issymbol():
            if the_atom_val == '=':
                new_atom = Atom(TokenItem(Token.QTEXT, '=')).asbuiltin()
                new_node = Node(NodeType.ATOM)
                new_node.add(new_atom)
                return new_node
            elif the_atom_val == '+':
                new_atom = Atom(TokenItem(Token.QTEXT, '+')).asbuiltin()
                new_node = Node(NodeType.ATOM)
                new_node.add(new_atom)
                return new_node
            elif the_atom_val == '*':
                new_atom = Atom(TokenItem(Token.QTEXT, '*')).asbuiltin()
                new_node = Node(NodeType.ATOM)
                new_node.add(new_atom)
                return new_node
        return maybe_node

    # parse_list: Stream<TokenItem> -> Node
    def parse_list(self, tokens):
        nx = len(tokens)
        if nx == 0:
            return None
        node = Node(NodeType.LIST) # should be more like NodeType.EXPR
        idx = 0
        tk = tokens[idx]
        while not tk.is_list_end():
            # One of: [IDENT, INTEGER, FLOAT, TEXT, BOOL]
            if tk.has_value(): 
                new_node = self.parse_atom(tk)
                if new_node != None:
                    adjusted_node = self.symbol_as_builtin(new_node)
                    node.add(adjusted_node)
    
            # One of: [LPAREN]
            elif tk.is_list_begin():
                idx = idx + 1
                maybe_list = self.parse_list(tokens[idx:])
                if maybe_list == None:
                    print("Unexpected end of sub-list")
                    return None
                sub_list, rest_tokens = maybe_list
                node.add(sub_list)
                idx = idx + len(sub_list) # + 1
            #...
    
            idx = idx + 1
            if idx >= len(tokens):
                print("Unexpected end of list")
                return None
            tk = tokens[idx]
            # tk_type = tk.t
    
        return node, tokens[idx+1:] # should be number of tokens consummed, not [1:]
   
    def parse_expr(self, tokens):
        # print("ENTERED parse_expr")
        # should see an Atom followed by LINE_END, or BINARY_OP or ASSIGN_OP
        # could see a LINE_BEGIN or a LINE_END anywhere 
        if len(tokens) == 0:
            return None
    
        # Make sure we have an actual Token
        tk = tokens[0]
        if tk is None:
            return None
    
        elif tk.is_line_end():
            self.clear_nodes()
            lx = len(tokens)
            if lx > 1:
                next_tk = tokens[1]
                if next_tk.is_line_begin():
                    if len(next_tk.value) > 0:
                        self.line = int(next_tk.value)
                    return self.parse_expr(tokens[2:])
            return self.parse_expr(tokens[1:])
        elif tk.is_line_begin():
            self.line = int(tk.value)
            return self.parse_expr(tokens[1:])
        else:
            maybe_node = self.parse_atom(tk)
            if maybe_node != None:
                adjusted_node = self.symbol_as_builtin(maybe_node)
                print("adjusted_node: ", adjusted_node)
                # If this atom is a BINARY_OP, 
                # establish a new Node,
                # pop its left argument from the node stack
                # append its right argument from the tokens ahead
                the_atom = adjusted_node.get_value()
                the_atom_val = the_atom.get_value()
                print("the_atom: ", the_atom)
                print("the_atom_val: ", the_atom_val)
                if the_atom.isfunction():
                    print("adjusted_node is a symbol: ", adjusted_node)
                    #if the_atom.get_value() == '=':
                    if the_atom_val == Builtin.OP_ASSIGN:
                        print('Found an assignment operator')
                        # establish a new node
                        node = Node(NodeType.LIST) # should be more like NodeType.EXPR
                        node.add(adjusted_node)

                        # pop left arg from stack (error if cant pop)
                        left_node = self.pop_node()
                        if left_node == None:
                            print("ERROR: No L-value provided for assignment %s: %d" % (self.filename, self.line))
                            return None
                        else:
                            print("LEFT_NODE was: ", left_node)
                        node.add(left_node)
                        parse_result = self.parse_expr(tokens[1:])
                        if parse_result != None:
                            right_node, more_tokens = parse_result
                            node.add(right_node)
                            print("RIGHT_NODE is: ", right_node)
                            return node, more_tokens
                        else:
                            print("RIGHT_NODE is not there...")
                            return None
                self.push_node(maybe_node)
                self.parse_expr(tokens[1:])
    
            # Update line info when provided
            # Must be a LIST - better check anyway
            elif tk.is_list_begin():
                # either returns None
                # or (node, [more_tokens])
                return self.parse_list(tokens[1:])
            else:
                if not tk is None:
                    print('Unexpected?(a): ', tk)
                    print('Unexpected?: ', str(tk))
                return None
        
        
    # parse_node: Stream<TokenItem> -> Node
    def parse_node(self, tokens):
        print("ENTERED parse_node")
        if len(tokens) == 0:
            return None
    
        # Make sure we have an actual Token
        tk = tokens[0]
        if tk is None:
            return None
    
        elif tk.is_line_end():
            lx = len(tokens)
            if lx > 1:
                next_tk = tokens[1]
                if next_tk.is_line_begin():
                    if len(next_tk.value) > 0:
                        self.line = int(next_tk.value)
                    return self.parse_node(tokens[2:])
            return self.parse_node(tokens[1:])
        elif tk.is_line_begin():
            self.line = int(tk.value)
            return self.parse_node(tokens[1:])
        else:
            maybe_node = self.parse_atom(tk)
            if maybe_node != None:
                adjusted_node = self.symbol_as_builtin(maybe_node)
                return adjusted_node, tokens[1:]
    
            # Update line info when provided
            # Must be a LIST - better check anyway
            elif tk.is_list_begin():
                # either returns None
                # or (node, [more_tokens])
                return self.parse_list(tokens[1:])
            else:
                if not tk is None:
                    print('Unexpected?(a): ', tk)
                    print('Unexpected?: ', str(tk))
                return None

# parse_program: FilePath -> Node[]
def new_parse_program(file_path):
    tokens = tokenize_program(file_path)
    tk_count = len(tokens)
    if tk_count > 0:
        print('%i ~new~ tokens found in "%s"' % (tk_count, file_path))

    all_nodes = []
    parseInfo = Parser()
    parseInfo.filename = file_path
    parsed_result = parseInfo.parse_expr(tokens)
    if parsed_result == None:
        print("1. parse_expr() returned: None")
    else:
        print("1. parse_expr() returned: ", parsed_result[0])
    while parsed_result != None:
        node, tokens = parsed_result
        if node == None:
            print("2. parse_expr() returned: None")
        else:
            print("2. parse_expr() returned: ", node)
        all_nodes.append(node)
        parsed_result = parseInfo.parse_expr(tokens)
    return all_nodes

def parse_program(file_path):
    tokens = tokenize_program(file_path)
    tk_count = len(tokens)
    if tk_count > 0:
        print('%i tokens found in "%s"' % (tk_count, file_path))

    all_nodes = []
    parseInfo = Parser()
    parseInfo.filename = file_path
    parsed_result = parseInfo.parse_node(tokens)
    while parsed_result != None:
        node, tokens = parsed_result
        all_nodes.append(node)
        parsed_result = parseInfo.parse_node(tokens)
    return all_nodes
