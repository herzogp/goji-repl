
# Parsing rules
from enum import Enum

from parser.symbols import SymbolType

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

class Rule:
    def __init__(self, binding_power, symbol_type, handler, handler_type):
        self._bp = binding_power
        self._ntype = symbol_type
        self._handler = handler
        self._htype = handler_type

    def __str__(self):
        rule_type = "Unknown"
        if self._htype == HandlerType.NULL_DENOTED:
            rule_type = "Null"
        elif self._htype == HandlerType.LEFT_DENOTED:
            rule_type = "Left"
        elif self._htype == HandlerType.STATEMENT_DENOTED:
            rule_type = "Stmt"
        return "%sRule(%s, %d)" % (rule_type, self._ntype, self._bp.value)

    @property
    def bp(self):
        return self._bp

    @property
    def symbol_type(self):
        return self._ntype

    @property
    def handler_type(self):
        return self._htype

    @property
    def handler(self):
        return self._handler

    def is_null_denoted(self):
        return self._htype == HandlerType.NULL_DENOTED

    def is_left_denoted(self):
        return self._htype == HandlerType.LEFT_DENOTED

    def is_statement_denoted(self):
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
    def __init__(self):
        self.null_rules = {}
        self.left_rules = {}
        self.stmt_rules = {}
        self.all_bps = {}

    def register_rule(self, rule):
        ntype = rule.symbol_type
        if isinstance(rule, NullRule):
            self.null_rules[ntype] = rule
        elif isinstance(rule, LeftRule):
            self.left_rules[ntype] = rule
        elif isinstance(rule, StatementRule):
            self.stmt_rules[ntype] = rule
        else:
            print("Unknown rule type: ", rule)
            return
        self.all_bps[ntype] = rule.bp
   
    def show_all_rules(self):
        for nt, r in self.null_rules.items():
            print("NULL: %s => %s" % (nt, r.bp))

        for nt, r in self.left_rules.items():
            print("LEFT: %s => %s" % (nt, r.bp))

        for nt, r in self.stmt_rules.items():
            print("STMT: %s => %s" % (nt, r.bp))

        print('')

    def null_rule_for_token_type(self, ntype):
        val = self.null_rules.get(ntype)
        #print("Using NullRule => %s" % val)
        if val is None:
            return None
        return val.handler
    
    def left_rule_for_token_type(self, ntype):
        val = self.left_rules.get(ntype)
        #print("Using LeftRule => %s" % val)
        if val is None:
            return None
        return val.handler
    
    def statement_rule_for_token_type(self, ntype):
        rule = self.stmt_rules.get(ntype)
        if rule == None:
            return None
        return rule.handler
    
    def bp_for_token_type(self, ntype):
        result = self.all_bps.get(ntype) 
        return result
