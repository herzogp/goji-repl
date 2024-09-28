from enum import Enum

from typing import Union, Any, cast

from tokenizer.tokens import (
    tokenitem_for_numeric,
    tokenitem_for_text,
    tokenitem_for_identifier,
    nil_token_item,
)


class SymbolType(Enum):

    # Literals
    LITERAL_INTEGER = 10
    LITERAL_FLOAT = 11
    LITERAL_STRING = 12
    IDENTIFIER = 13
    LITERAL_BOOL = 14  # 'true' | 'false'

    # Scoping
    LEFT_BRACKET = 20  # '['
    RIGHT_BRACKET = 21  # ']'
    LEFT_BRACE = 22  # '{'
    RIGHT_BRACE = 23  # '}'
    LEFT_PAREN = 24  # '('
    RIGHT_PAREN = 25  # ')'

    # Math Operations
    OP_ADD = 31  # '+'
    OP_MULTIPLY = 32  # '*'
    OP_SUBTRACT = 33  # '-'
    OP_DIVIDE = 34  # '/'
    OP_MODULO = 35  # '%'

    # Assignment
    OP_ASSIGN = 40  # '='

    # Indexing
    COMMA = 50  # ','

    # Meta Info
    LINE_END = 1002
    INPUT_END = 1003

    LITERAL_NIL = 2000


# _typ : SymbolType
# _val : native repr
# _lno : source line number
# _col : source column number
class SymToken:
    def __init__(self, token_item) -> None:
        self._val: Any = None
        token_val = token_item.value
        if token_item.is_text():
            if token_val == "true":
                self._typ = SymbolType.LITERAL_BOOL
                self._val = True
            elif token_val == "false":
                self._typ = SymbolType.LITERAL_BOOL
                self._val = False
            # elif other builtin reserved or keywords
            else:
                self._typ = SymbolType.IDENTIFIER
                self._val = token_val

        elif token_item.is_literal_text():
            self._typ = SymbolType.LITERAL_STRING
            self._val = token_val

        elif token_item.is_numeric():
            if token_val.find("0x") == 0:
                self._typ = SymbolType.LITERAL_INTEGER  # (or FLOAT)
                self._val = int(token_val, 16)
            elif (token_val.find(".") >= 0) or (token_val.find("e") > 0):
                self._typ = SymbolType.LITERAL_FLOAT
                self._val = float(token_val)
            else:
                self._typ = SymbolType.LITERAL_INTEGER  # (or FLOAT)
                self._val = int(token_val)

        elif token_item.is_list_begin():
            self._typ = SymbolType.LEFT_PAREN
            self._val = "("

        elif token_item.is_list_end():
            self._typ = SymbolType.RIGHT_PAREN
            self._val = ")"

        elif token_item.is_symbol():
            self._val = token_val
            if token_val == "+":
                self._typ = SymbolType.OP_ADD
            elif token_val == "-":
                self._typ = SymbolType.OP_SUBTRACT
            elif token_val == "*":
                self._typ = SymbolType.OP_MULTIPLY
            elif token_val == "/":
                self._typ = SymbolType.OP_DIVIDE
            elif token_val == "%":
                self._typ = SymbolType.OP_MODULO
            elif token_val == "=":
                self._typ = SymbolType.OP_ASSIGN
            elif token_val == "(":
                self._typ = SymbolType.LEFT_PAREN
            elif token_val == ")":
                self._typ = SymbolType.RIGHT_PAREN
            elif token_val == "[":
                self._typ = SymbolType.LEFT_BRACKET
            elif token_val == "]":
                self._typ = SymbolType.RIGHT_BRACKET
            elif token_val == "{":
                self._typ = SymbolType.LEFT_BRACE
            elif token_val == "}":
                self._typ = SymbolType.RIGHT_BRACE
            elif token_val == ",":
                self._typ = SymbolType.COMMA
            elif token_val == "":
                print("created a nil SymToken")
                self._typ = SymbolType.LITERAL_NIL
            # ----------------------------------------------------------------------
            # elif other symbols from this list of 16:
            # ! @ # $ ^ & ; : | \\ ? > < , .
            # ----------------------------------------------------------------------

        elif token_item.is_line_end():
            self._typ = SymbolType.LINE_END
            self._val = ""
        elif token_item.is_input_end():
            self._typ = SymbolType.INPUT_END
            self._val = ""
        else:
            print("UNABLE to determine what SymToken to create")
            self._typ = SymbolType.LITERAL_NIL
            self._val = ""
        self._lno = token_item.line
        self._col = token_item.col

    def __str__(self) -> str:
        base_name = "SymbolType.%s" % self._typ.name
        loc_info = "[%d:%d]" % (self._lno, self._col)
        if self._val != "":
            base_name = "%s(%s)" % (base_name, self._val)
        return "%s%s" % (base_name, loc_info)

    @property
    def symtype(self) -> SymbolType:
        return self._typ

    @property
    def symvalue(self) -> Union[str, int, float, bool]:
        return self._val

    @property
    def line(self) -> int:
        return self._lno

    @property
    def col(self) -> int:
        return self._col

    def as_str(self, def_value: str) -> str:
        if self.is_string() or self.is_ident():
            return cast(str, self._val)
        print("is not a string: ", self)
        return def_value

    def is_integer(self) -> bool:
        return self._typ == SymbolType.LITERAL_INTEGER

    def is_float(self) -> bool:
        return self._typ == SymbolType.LITERAL_FLOAT

    def is_bool(self) -> bool:
        return self._typ == SymbolType.LITERAL_BOOL

    def is_string(self) -> bool:
        return self._typ == SymbolType.LITERAL_STRING

    def is_ident(self) -> bool:
        return self._typ == SymbolType.IDENTIFIER

    def is_input_end(self) -> bool:
        return self._typ == SymbolType.INPUT_END

    def is_line_end(self) -> bool:
        return self._typ == SymbolType.LINE_END

    def is_nil(self) -> bool:
        return self._typ == SymbolType.LITERAL_NIL


def symbolized(tokens) -> list[SymToken]:
    sym_tokens = []
    for tk_item in tokens:
        sym_tokens.append(SymToken(tk_item))
    return sym_tokens


nil_symtoken = SymToken(nil_token_item)


def symtoken_for_numeric(val) -> SymToken:
    token_item = tokenitem_for_numeric(val)
    return SymToken(token_item)


def symtoken_for_text(val) -> SymToken:
    token_item = tokenitem_for_text(val)
    return SymToken(token_item)


def symtoken_for_identifier(val) -> SymToken:
    token_item = tokenitem_for_identifier(val)
    return SymToken(token_item)
