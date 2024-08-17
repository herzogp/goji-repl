import os
import itertools
from enum import Enum

from tokenizer_tools import lines_to_process

class Token(Enum):
    UNKNOWN = 0 # Unexpected lexical finding

    # List
    LIST_BEGIN = 1 # '('
    LIST_END = 2 # ')'

    # plain text
    TEXT = 3 

     # Quoted text
    QTEXT = 4

    # Digits '0', '1',  ..., '9'', '.'
    NUMERIC = 5 
    
    # any of "!@#$%^&*-+=[]{};:|\\?><,./" 
    # Must not be the lead character for a TEXT, QTEXT, NUMBER
    SYMBOL = 6 

# ------------------------------------------------------------
# TokenItem {
#   t Token
#   v string # Empty for LPAREN snd RPAREN
# }
# ------------------------------------------------------------
class TokenItem:
    def __init__(self, tk, ch=''):
        self.t = tk
        self.v = ch

    def __str__(self):
        name = self.t.name
        val = self.v
        msg = name
        if self.has_value():
            msg = "%s(%s)" % (name, val)
        return msg

    def has_value(self):
        return self.t == Token.TEXT \
            or self.t == Token.QTEXT \
            or self.t == Token.SYMBOL \
            or self.t == Token.NUMERIC

    def is_numeric(self):
        return self.t == Token.NUMERIC
    
    def is_text(self):
        return self.t == Token.TEXT

    def is_literal_text(self):
        return self.t == Token.QTEXT

    def is_symbol(self):
        return self.t == Token.SYMBOL

    def is_list_begin(self):
        return self.t == Token.LIST_BEGIN

    def is_list_end(self):
        return self.t == Token.LIST_END

    def value(self):
        return self.v

    def name(self):
        return self.t.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

class ScanContext(Enum):
    IN_NOTHING = 0
    IN_SINGLE_QUOTE = 1
    IN_DOUBLE_QUOTE = 2
    IN_TEXT = 3
    IN_NUMERIC = 4

# ----------------------------------------------------------------------
# Tokenizer {
#   tk_type # Type of token for which characters are being collected
#              # Will never be Token.LPAREN or Token.RPAREN
#   text       # Collected characters (so far)
#   tokens     # List of TokenItem's scanned (so far)
# }
# ----------------------------------------------------------------------
class Tokenizer:

    def __init__(self):
        self.tk_type = Token.UNKNOWN
        self.text = ''
        self.tokens = [] # TokenItem[]
        self.state = ScanContext.IN_NOTHING
        self.info = {}
        self.valid_symbols = "!@#$%^&*-+=[]{};:|\\?><,./"
        self.single_quote = "'"
        self.double_quote = '"'
        self.digits = "0123456789"
        self.hexdigits = "AaBbCcDdEeFf"

    def reset(self):
        self.tk_type = Token.UNKNOWN
        self.text = ''
        self.state = ScanContext.IN_NOTHING
        self.info = {}

    def istext(self, char):
        return char.isalpha()

    def isnumeric(self, char):
        return self.digits.find(char) >= 0

    def ishexdigit(self, char):
        return self.hexdigits.find(char) >= 0

    def issymbol(self, char):
        return self.valid_symbols.find(char) >= 0

    def istoken(self):
        return self.tk_type != Token.UNKNOWN

    def get_text(self):
        return self.text

    def get_tokens(self):
        return self.tokens

    def add_token(self, tk, s=''):
        self.tokens.append(TokenItem(tk, s))
        self.reset()

    def emit_token(self):
        if self.istoken():
            self.add_token(self.tk_type, self.text)

    def did_handle_undetermined(self, char):
        if char == '(':
            self.add_token(Token.LIST_BEGIN)
        elif char == ')':
            self.add_token(Token.LIST_END)
        elif self.issymbol(char):
            self.add_token(Token.SYMBOL, char)
        elif char == self.double_quote:
            self.state = ScanContext.IN_DOUBLE_QUOTE
            self.tk_type = Token.QTEXT
        elif char == self.single_quote:
            self.state = ScanContext.IN_SINGLE_QUOTE
            self.tk_type = Token.QTEXT
        elif self.isnumeric(char):
            self.state = ScanContext.IN_NUMERIC
            self.tk_type = Token.NUMERIC
            self.text = char
        elif char.isalpha():
            self.state = ScanContext.IN_TEXT
            self.tk_type = Token.TEXT
            self.text = char
        elif char.isspace():
            return True
        else:
            self.add_token(Token.SYMBOL, char)
        return True

    def did_handle_quoted(self, char, closing_char):
        if 'is_raw' in self.info:
            self.text = self.text + char
            del self.info['is_raw']
            return True
        if char == '\\':
            self.info['is_raw'] = True
            return True
        if char == closing_char:
            self.emit_token()
        else:
            self.text = self.text + char
        return True

    def did_handle_text(self, char):
        if char.isalpha() or self.isnumeric(char) or (char == '_'):
            self.text = self.text + char
        else:
            self.emit_token()
            return False
        return True
        
    def did_handle_numeric(self, char):
        if self.isnumeric(char):
            self.text = self.text + char
            return True
        if (self.text == '0') and (char == 'x'):
            self.info['is_hex'] = True
            self.info['is_exp'] = False # prevent confusion with 'E' or 'e'
            return True
        if 'is_hex' in self.info:
            if self.ishexdigit(char):
                self.text = self.text + char
                return True
            else:
                self.emit_token()
                return False

        if (char == 'e') or (char == 'E'):
            if 'is_exp' not in self.info:
                if 'seen_dot' in self.info:
                    del self.info['seen_dot']
                self.info['is_exp'] = True
                self.text = self.text + 'e' # normalize by converting 'E' to 'e'
                return True
            else:
                self.emit_token()
                return False
        
        if char == '.':
            if 'seen_dot' not in self.info:
                self.info['seen_dot'] = True
                self.text = self.text + char
                return True
            else:
                self.emit_token()
                return False

        if (char == '-') or (char == '+'):
            if self.text.endswith('e'):
                self.text = self.text + char
            else:
                self.emit_token()
                return False

        self.emit_token()
        return False

    def did_handle_char(self, char):
        state = self.state
        if state == ScanContext.IN_NOTHING:
            return self.did_handle_undetermined(char)
        elif state == ScanContext.IN_DOUBLE_QUOTE:
            return self.did_handle_quoted(char, self.double_quote)
        elif state == ScanContext.IN_SINGLE_QUOTE:
            return self.did_handle_quoted(char, self.single_quote)
        elif state == ScanContext.IN_TEXT:
            return self.did_handle_text(char)
        elif state == ScanContext.IN_NUMERIC:
            return self.did_handle_numeric(char)
        else:
            print('Unknown state: "%s"' % state.name)
        return True

# ----------------------------------------------------------------------
# End class Tokekenizer
# ----------------------------------------------------------------------

def tokenize(char_iter):    
    tk = Tokenizer()

    # Iterate over the characters
    for char in char_iter:
        handled = False
        while not handled:
            handled = tk.did_handle_char(char)

    # Done with all chars being handled somehow
    # Drain the tokenizer
    if tk.istoken():
        tk.emit_token()

    return tk.get_tokens()

def tokenize_program(file_path):
    joined_lines = lines_to_process(file_path)
    if len(joined_lines) == 0:
        print('Unable to read any lines from "%s"' % file_path)
    char_iter = itertools.islice(joined_lines, 0, None)
    return tokenize(char_iter)
