from typing import Union

from options import GojiOptions

from tokenizer.tokens import (
    tokenize_program,
    TokenItem,
)

from parser.parser import Parser

from parser.symbols import (
    SymbolType,
    SymToken,
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

from ast.interfaces import Stmt

class FileParser:
    def __init__(self, filename: str, tokens: list[TokenItem], all_lines: list[str]) -> None:
        self._filename = filename
        self._line = 0
        self._symtokens = symbolized(tokens)
        self._all_lines = all_lines
        self._ntx = len(self._all_lines)

    def show_symtokens(self) -> None:
        print("")
        idx = 0
        for symtok in self._symtokens:
            print("[%2d] %s" % (idx, symtok))
            idx = idx + 1
        print("")

    @property
    def filename(self) -> str:
        return self._filename

    @filename.setter
    def filename(self, value: str) -> None:
        self._filename = value

    @property
    def line(self) -> int:
        return self._line

    @line.setter
    def line(self, value: int) -> None:
        self._line = value

    def has_line_numbers(self) -> bool:
        return self._line > 0

    def source_line(self, one_based_lno: int) -> str:
        idx = one_based_lno - 1
        if idx < 0 or idx >= self._ntx:
            return '<line %d not found>' % one_based_lno
        return self._all_lines[idx]

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
    def parse(self, options: GojiOptions) -> list[Stmt]:
        body = []
        p = Parser(self._symtokens, self._all_lines, options)
        while p.has_tokens():
            symtoken = p.current_token()
            if not symtoken is None:
                st = parse_statement(p, self.source_line(symtoken.line))
                if not st is None:
                    body.append(st)
        return body

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


def pratt_parse_program(file_path: str, options: GojiOptions) -> tuple[list[Stmt], list[str]]:
    tokens, all_lines = tokenize_program(file_path)
    tk_count = len(tokens)
    if tk_count > 0 and options.show_tokens:
        print('%i <Pratt> tokens found in "%s"' % (tk_count, file_path))
    parseInfo = FileParser(file_path, tokens, all_lines)
    if options.show_tokens:
        parseInfo.show_symtokens()
    parsed_result = parseInfo.parse(options)
    print("parsing completed")
    print("")
    return (parsed_result, all_lines)
