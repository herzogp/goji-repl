
# Parsing rules
# 
# var bp_lu = bp_lookup{}
# var nud_lu = nud_lookup{}
# var led_lu = led_lookup{}
# var stmt_lu =stmt_lookup{}
# 
# 
# func led (kind lexer.TokenKind, bp binding_power, led_fn led_handler) {
# 	bp_lu[kind] = bp
# 	led_lu[kind] = led_fn
# }
# 
# func nud (kind lexer.TokenKind, bp binding_power, nud_fn nud_handler) {
# 	bp_lu[kind] = primary
# 	nud_lu[kind] = nud_fn
# }
# 
# func stmt (kind lexer.TokenKind, stmt_fn stmt_handler) {
# 	bp_lu[kind] = defalt_bp
# 	stmt_lu[kind] = stmt_fn
# }
from enum import Enum

class BindingPower(Enum):
	DEFAULT_BP = 0
	COMMA = 1
	ASSIGNMENT = 2
	LOGICAL = 3
	RELATIONAL = 4
	ADDITIVE = 5
	MULTIPLICATIVE = 6
	UNARY = 7
	CALL = 8
	MEMBER = 9
	PRIMARY = 10

class HandlerType(Enum):
    NULL_DENOTED = 0
    LEFT_DENOTED = 1
    STATEMENT_DENOTED = 2

class Rule:
    def __init__(self, binding_power, node_type, handler, handler_type):
        self._bp = binding_power
        self._ntype = node_type
        self._handler = handler
        self._htype = handler_type

    @property
    def bp(self):
        return self._bp

    @property
    def node_type(self):
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
    def __init__(self, binding_power, node_type, handler):
        super().__init__(binding_power, node_type, handler, HandlerType.NULL_DENOTED)

class LeftRule(Rule):
    def __init__(self, binding_power, node_type, handler):
        super().__init__(binding_power, node_type, handler, HandlerType.LEFT_DENOTED)
        
class StatementRule(Rule):
    def __init__(self, binding_power, node_type, handler):
        super().__init__(binding_power, node_type, handler, HandlerType.STATEMENT_DENOTED)

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
        self.statement_rules = {}
        self.all_bps = {}

    def register_rule(self, rule):
        ntype = rule.node_type
        if isinstance(rule, NullRule):
            self.null_rules[ntype] = rule
        elif isinstance(rule, LeftRule):
            self.left_rules[ntype] = rule
        elif isinstance(rule, StatementRule):
            self.statement_rules[ntype] = rule
        else:
            print("Unknown rule type: ", rule)
            return
        self.all_bps[ntype] = rule.bp
    
    def null_rule_for_token_type(self, ntype):
        return self.null_rules.get(ntype).handler
    
    def left_rule_for_token_type(self, ntype):
        return self.left_rules.get(ntype).handler
    
    def statement_rule_for_token_type(self, ntype):
        rule = self.statement_rules.get(ntype)
        if rule == None:
            print("No statement rule found for %s" % ntype)
            return None
        return rule.handler
    
    def bp_for_token_type(self, ntype):
        result = self.all_bps.get(ntype) 
        if result == None:
            result = -1
        return result

