from typing import Union

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
    def __init__(self, filename: str, tokens: list[TokenItem]) -> None:
        self._filename = filename
        self._line = 0
        self._symtokens = symbolized(tokens)
        # self._rule_provider = create_rule_provider()

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
    def parse(self) -> list[Stmt]:
        # parsed_result = parseInfo.parse_expr(self.tokens)
        body = []
        # p = Parser(self._symtokens, self._rule_provider)
        p = Parser(self._symtokens)
        while p.has_tokens():
            st = parse_statement(p)
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


def pratt_parse_program(file_path: str) -> None:
    tokens = tokenize_program(file_path)
    tk_count = len(tokens)
    if tk_count > 0:
        print('%i <Pratt> tokens found in "%s"' % (tk_count, file_path))
    parseInfo = FileParser(file_path, tokens)
    parseInfo.show_symtokens()
    parsed_result = parseInfo.parse()

# def create_rule_provider() -> RuleProvider:
# 
#     rule_provider = RuleProvider()
# 
#     # Literals & Symbols
#     all_literals = [
#         SymbolType.LITERAL_INTEGER,
#         SymbolType.LITERAL_FLOAT,
#         SymbolType.LITERAL_STRING,
#         SymbolType.LITERAL_BOOL,
#         SymbolType.IDENTIFIER,
#     ]
#     bp = BindingPower.PRIMARY
#     for x in all_literals:
#         rule_provider.register_rule(NullRule(bp, x, parse_primary_expr))
# 
#     # Math Operations
#     rule_provider.register_rule(LeftRule(BindingPower.ADDITIVE, SymbolType.OP_ADD, parse_binary_expr))
#     rule_provider.register_rule(LeftRule(BindingPower.MULTIPLICATIVE, SymbolType.OP_MULTIPLY, parse_binary_expr))
# 
#     # Assignment
#     rule_provider.register_rule(LeftRule(BindingPower.ASSIGNMENT, SymbolType.OP_ASSIGN, parse_assignment_expr))
# 
#     # Grouping and Scope
#     rule_provider.register_rule(NullRule(BindingPower.DEFAULT_BP, SymbolType.LEFT_PAREN, parse_grouping_expr))
# 
#     return rule_provider

# Moved to parser/expressions.py
# global_rule_provider = create_rule_provider()
