
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
    def __init__(self, binding_power, node_type, handler, NULL_DENOTED):
        super().__init__(binding_power, node_type)

class LeftRule(Rule):
    def __init__(self, binding_power, node_type, handler, LEFT_DENOTED):
        super().__init__(binding_power, node_type)
        
class StatementRule(Rule):
    def __init__(self, binding_power, node_type, handler, STATEMENT_DENOTED):
        super().__init__(binding_power, node_type)

# ----------------------------------------------------------------------
# NodeType Handlers
# ----------------------------------------------------------------------
# null_handler: Parser -> ast.Expr
# left_handler  Parser -> ast.Expr -> bp BindingPower -> ast.Expr
# statement_handler Parser -> ast.Stmt
# ----------------------------------------------------------------------

null_rules = {}
left_rules = {}
statement_rules = {}
all_bps = {}

def register_rule(rule):
    ntype = rule.node_type
    if isinstance(rule, NullRule):
        null_rules[ntype] = rule
    elif isinstance(rule, LeftRule):
        left_rules[ntype] = rule
    elif isinstance(rule, StatementRule):
        statement_rules[ntype] = rule
    else:
        print("Unknown rule type: ", rule)
        return
    all_bps[ntype] = rule.binding_power

def null_rule_for_token_type(ntype):
    return null_rules.get(ntype)

def left_rule_for_token_type(ntype):
    return left_rules.get(ntype)

def statement_rule_for_token_type(ntype):
    return statement_rules.get(ntype)

def bp_for_token_type(ntype):
    result = all_bps.get(ntype) 
    if result == None:
        result = -1
    return result
    return 

