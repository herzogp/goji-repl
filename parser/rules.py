
from typing import Union, Callable, cast
from enum import Enum

from ast.interfaces import Expr, Stmt

from parser.symbols import SymbolType

from parser.driver import Parser

class BindingPower(Enum):
	DEFAULT_BP = 0
	COMMA = 10
	ASSIGNMENT = 20
	LOGICAL = 30
	RELATIONAL = 40
	ADDITIVE = 50
	MULTIPLICATIVE = 60
	UNARY = 70
	CALL = 80
	MEMBER = 90
	PRIMARY = 100

class HandlerType(Enum):
    NULL_DENOTED = 0
    LEFT_DENOTED = 1
    STATEMENT_DENOTED = 2

NullHandler = Callable[[Parser], Expr]
LeftHandler = Callable[[Parser, Expr, BindingPower], Expr]
StmtHandler = Callable[[Parser], Stmt]

# null_handler: Parser -> ast.Expr
# left_handler  Parser -> ast.Expr -> bp BindingPower -> ast.Expr
# statement_handler Parser -> ast.Stmt
RuleHandler = Union[NullHandler, LeftHandler, StmtHandler]

class Rule:
    def __init__(self, binding_power: BindingPower, symbol_type: SymbolType, handler: RuleHandler, handler_type: HandlerType) -> None:
        self._bp = binding_power
        self._ntype = symbol_type
        self._handler = handler
        self._htype = handler_type

    def __str__(self) -> str:
        rule_type = "Unknown"
        if self._htype == HandlerType.NULL_DENOTED:
            rule_type = "Null"
        elif self._htype == HandlerType.LEFT_DENOTED:
            rule_type = "Left"
        elif self._htype == HandlerType.STATEMENT_DENOTED:
            rule_type = "Stmt"
        return "%sRule(%s, %d)" % (rule_type, self._ntype, self._bp.value)

    @property
    def bp(self) -> BindingPower:
        return self._bp

    @property
    def symbol_type(self) -> SymbolType:
        return self._ntype

    @property
    def handler_type(self) -> HandlerType:
        return self._htype

    @property
    def handler(self) -> RuleHandler:
        return self._handler

    def is_null_denoted(self) -> bool:
        return self._htype == HandlerType.NULL_DENOTED

    def is_left_denoted(self) -> bool:
        return self._htype == HandlerType.LEFT_DENOTED

    def is_statement_denoted(self) -> bool:
        return self._htype == HandlerType.STATEMENT_DENOTED

class NullRule(Rule):
    def __init__(self, binding_power, symbol_type, handler):
        super().__init__(binding_power, symbol_type, handler, HandlerType.NULL_DENOTED)

class LeftRule(Rule):
    def __init__(self, binding_power, symbol_type, handler):
        super().__init__(binding_power, symbol_type, handler, HandlerType.LEFT_DENOTED)
        
class StatementRule(Rule):
    def __init__(self, binding_power, symbol_type, handler):
        super().__init__(binding_power, symbol_type, handler, HandlerType.STATEMENT_DENOTED)

# ----------------------------------------------------------------------
# NodeType Handlers
# ----------------------------------------------------------------------
# null_handler: Parser -> ast.Expr
# left_handler  Parser -> ast.Expr -> bp BindingPower -> ast.Expr
# statement_handler Parser -> ast.Stmt
# ----------------------------------------------------------------------
class RuleProvider:
    def __init__(self) -> None:
        self.null_rules: dict[SymbolType, NullRule] = {}
        self.left_rules: dict[SymbolType, LeftRule] = {}
        self.stmt_rules: dict[SymbolType, StatementRule] = {}
        self.all_bps: dict[SymbolType, BindingPower] = {}

    def register_rule(self, rule: Rule) -> None:
        ntype = rule.symbol_type
        if isinstance(rule, NullRule):
            self.null_rules[ntype] = cast(NullRule, rule)
        elif isinstance(rule, LeftRule):
            self.left_rules[ntype] = cast(LeftRule, rule)
        elif isinstance(rule, StatementRule):
            self.stmt_rules[ntype] = cast(StatementRule, rule)
        else:
            print("Unknown rule type: ", rule)
            return
        self.all_bps[ntype] = rule.bp
   
    def show_all_rules(self) -> None:
        for nt, null_rule in self.null_rules.items():
            print("NULL: %s => %s" % (nt, null_rule.bp))

        for nt, left_rule in self.left_rules.items():
            print("LEFT: %s => %s" % (nt, left_rule.bp))

        for nt, stmt_rule in self.stmt_rules.items():
            print("STMT: %s => %s" % (nt, stmt_rule.bp))

        print('')

    def null_rule_for_token_type(self, ntype: SymbolType) -> Union[NullHandler, None]:
        val = self.null_rules.get(ntype)
        if val is None:
            return None
        return cast(NullHandler, val.handler)
    
    def left_rule_for_token_type(self, ntype: SymbolType) -> Union[LeftHandler, None]:
        val = self.left_rules.get(ntype)
        if val is None:
            print("left_rule lookup: Unable to get val for ntype: ", ntype)
            return None
        return cast(LeftHandler, val.handler)
    
    def statement_rule_for_token_type(self, ntype: SymbolType) -> Union[StmtHandler, None]:
        rule = self.stmt_rules.get(ntype)
        if rule is None:
            return None
        return cast(StmtHandler, rule.handler)
    
    def bp_for_token_type(self, ntype):
        result = self.all_bps.get(ntype) 
        return result

