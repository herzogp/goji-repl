from tokenizer.tokens import (
    tokenize_program,
)

from parser.rules import (
    BindingPower,
    register_rule,
)

from parser.symbols import (
    SymbolType,
    symbolized,
)

from parser.expressions import (
    parse_primary_expr,
    parse_binary_expr,
    parse_assignment_expr,
    parse_grouping_expr,
)

from parser.statements import (
    parse_statement,
)

class FileParser:
    def __init__(self, filename, tokens):
        self._filename = filename
        self._line = 0
        self._symtokens = symbolized(tokens)

    def show_symtokens(self):
        print("")
        idx = 0
        for symtok in self._symtokens:
            print("[%2d] %s" % (idx, symtok))
            idx = idx + 1
        print("")

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
        self._line = value

    def has_line_numbers(self):
        return self._line > 0

    #----------------------------------------------------------------------
    # Top-level function
    #----------------------------------------------------------------------
    # DoParse: tokens[] -> ast.BlockStatement
    #
    # 0. declare Body ast.Statement[] # empty list
    #
    # 1. register all rules
    #
    # 2. instantiate a Parser 'p' (with these tokens)
    #
    # 3. while p.has_tokens():
    #    st = parse_stmt(p)
    #    body.append(st)
    #
    # 4. return st.BlockStatement(body)
    # p.parse_stmt()
    #----------------------------------------------------------------------
    def parse(self):
        # parsed_result = parseInfo.parse_expr(self.tokens)
        body = []
        p = Parser(self._symtokens)
        while p.has_tokens():
            st = parse_statement(p)
            body.append(st)
        return body

class Parser:
    def __init__(self, symtokens):
        self._symtokens = symtokens
        self._pos = 0
        self._ntx = len(symtokens)

    def has_tokens(self):
        return self._pos < self._ntx

    def current_token(self):
        if not self.has_tokens:
            print("current_token() -> None")
            return None
        print("current_token() -> %s" % self._symtokens[self._pos])
        return self._symtokens[self._pos]

    def peek_prev_token(self):
        idx = self._pos - 1
        if idx >= 0:
            symtok = self._symtokens[idx]
            return symtok
        return None

    def peek_next_token(self):
        idx = self._pos + 1
        if idx < self._ntx:
            symtok = self._symtokens[idx]
            return symtok
        return None

    def skip_one(self, type_to_skip, err_msg=''):
        symtok = self.current_token()
        if symtok.symtype != type_to_skip:
            if err_msg == '':
                err_msg = "Expected %s - saw %s" % (type_to_skip.name, symtok)
            raise Exception(err_msg)
        p.advance()

    def advance(self):
        oldpos = self._pos
        idx = self._pos + 1
        if idx <= self._ntx:
            self.pos = idx
        print("advance: %d to %d" % (oldpos, self.pos))
        return

# ---------------------------------------------------------------------- 
# Literals
# 	[ ] NULL
# 	[x] TRUE
# 	[x] FALSE
# 	[x] NUMBER
# 	[x] STRING
# 	[x] IDENTIFIER
# 
# Grouping & Scope
# 	[ ] EOF
# 	[x] OPEN_BRACKET
# 	[x] CLOSE_BRACKET
# 	[x] OPEN_CURLY
# 	[x] CLOSE_CURLY
# 	[x] OPEN_PAREN
# 	[x] CLOSE_PAREN
# 
# Statements
# 	[x] ASSIGNMENT
# 
# Conditional
# 	[ ] EQUALS
# 	[ ] NOT_EQUALS
# 	[ ] LESS
# 	[ ] LESS_EQUALS
# 	[ ] GREATER
# 	[ ] GREATER_EQUALS
# 
# Logical
# 	[ ] NOT
# 	[ ] OR
# 	[ ] AND
# 
# Symbolic Operations
# 	[ ] DOT
# 	[ ] DOT_DOT
# 	[ ] SEMI_COLON
# 	[ ] COLON
# 	[ ] QUESTION
# 	[ ] COMMA
# 
# Multi-Symbol Operations
#   [ ] PLUS_PLUS
#   [ ] MINUS_MINUS
#   [ ] PLUS_EQUALS
#   [ ] MINUS_EQUALS
#   [ ] NULLISH_ASSIGNMENT # ??=
# 
# Math Ops
#   [x] PLUS
#   [ ] DASH
#   [ ] SLASH
#   [x] STAR
#   [ ] PERCENT
# 
# Reserved Keywords
# 	[ ] LET
# 	[ ] CONST
# 	[ ] CLASS
# 	[ ] NEW
# 	[ ] IMPORT
# 	[ ] FROM
# 	[ ] FN
# 	[ ] IF
# 	[ ] ELSE
# 	[ ] FOREACH
# 	[ ] WHILE
# 	[ ] FOR
# 	[ ] EXPORT
# 	[ ] TYPEOF
# 	[ ] IN
# 
# Misc
# 	[ ] NUM_TOKENS


def setup_rules():

    # Literals & Symbols
    all_literals = [
        SymbolType.LITERAL_INTEGER,
        SymbolType.LITERAL_FLOAT,
        SymbolType.LITERAL_STRING,
        SymbolType.LITERAL_BOOL,
        SymbolType.IDENTIFIER,
    ]
    bp = BindingPower.PRIMARY
    for x in all_literals:
        register_rule(NullRule(bp, x, parse_primary_expr))

    # Math Operations
    register_rule(LeftRule(BindingPower.ADDITIVE, SymbolType.OP_ADD, parse_binary_expr))
    register_rule(LeftRule(BindingPower.MULTIPLICATIVE, SymbolType.OP_MULTIPLY, parse_binary_expr))

    # Assignment
    register_rule(LeftRule(BindingPower.ASSIGNMENT, SymbolType.OP_ASSIGN, parse_assignment_expr))

    # Grouping and Scope
    register_rule(NullRule(BindingPower.DEFAULT_BP, SymbolType.LEFT_PAREN, parse_grouping_expr))

def pratt_parse_program(file_path):
    tokens = tokenize_program(file_path)
    tk_count = len(tokens)
    if tk_count > 0:
        print('%i <Pratt> tokens found in "%s"' % (tk_count, file_path))
    parseInfo = FileParser(file_path, tokens)
    parseInfo.show_symtokens()
    parsed_result = parseInfo.parse()



