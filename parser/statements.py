# statement.py

from typing import Union

from parser.rules import (
    RuleProvider,
    BindingPower,
    StmtHandler,
    StatementRule,
)

from logging import (
    print_info,
    print_note,
    print_warning,
    print_error,
)

from parser.expressions import (
    parse_expr,
)

from ast.statements import (
    ExpressionStmt,
    BlockStmt,
)

from ast.interfaces import Stmt

from parser.driver import Parser

from parser.symbols import SymbolType

# Parser -> ast.Stmt
def parse_statement(p: Parser) -> Union[Stmt, None]:
    symtok = p.current_token()
    if symtok is None:
        return None
    rp = p.rule_provider
    stmt_rule = rp.statement_rule_for_token_type(symtok.symtype)
    if stmt_rule is None:
        line_number = symtok.line
        expression = parse_expr(p, BindingPower.DEFAULT_BP)
        p.skip_one(SymbolType.LINE_END)    
        if (expression is None): # or (symtok.isinputend()):
            if line_number > 0:
                print("[%2d] %s" % (line_number, p.source_line(line_number)))
                print("")
            return None
        # p.skip_one(SymbolType.LINE_END)    
        return ExpressionStmt(expression)
    return stmt_rule(p)

def parse_block_stmt(p: Parser) -> Union[Stmt, None]:
    p.skip_one(SymbolType.LEFT_BRACE)
    body: list[Stmt] = []

    while p.has_tokens():
        symtoken = p.current_token()
        if symtoken is None:
            return None # unexpected end of body
        if symtoken != SymbolType.RIGHT_BRACE:
            st = parse_statement(p)
            if st is None:
                print_error("*** Unable to parse_statement")
            else:
                print_info("Stmt: %s" % st)
                body.append(st)
        # p.advance()

    p.skip_over(SymbolType.RIGHT_BRACE)
    return BlockStmt(body)

def init_stmt_rules(rp: RuleProvider) -> None:
    rp.register_rule(StatementRule(BindingPower.DEFAULT_BP, SymbolType.LEFT_BRACE, parse_block_stmt))

