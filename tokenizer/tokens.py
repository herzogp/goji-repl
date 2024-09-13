import os
import itertools
from enum import Enum

from tokenizer.tools import lines_to_process

class Token(Enum):
    INPUT_END = 0 # Unexpected lexical finding

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

    # Source 
    LINE_END = 7 # ''

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
        self._lno  = 0
        self._col  = 0

    def __str__(self):
        name = self.t.name
        val = self.v
        body = name
        if self.has_value():
            body = "%s(%s)" % (name, val)
        
        if self._lno == 0:
            return body
        line_info = "[%d:%d]" % (self._lno, self._col)
        return "%s%s" % (body, line_info)

    def set_meta(self, line, col):
        self._lno = line
        self._col = col
        return self

    @property
    def line(self):
        return self._lno

    @property
    def col(self):
        return self._col

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

    def is_line_end(self):
        return self.t == Token.LINE_END

    def is_input_end(self):
        return self.t == Token.INPUT_END

    @property
    def value(self):
        return self.v

    @property
    def name(self):
        return self.t.name

    def __eq__(self, other):
        if isinstance(other, self.__class__):
            return self.__dict__ == other.__dict__
        else:
            return False

def tokenitem_for_numeric(val):
    return TokenItem(Token.NUMERIC, str(val))

def tokenitem_for_text(val):
    return TokenItem(Token.QTEXT, str(val))

def tokenitem_for_identifier(val):
    return TokenItem(Token.TEXT, str(val))

nil_token_item = TokenItem(Token.SYMBOL)

class ScanContext(Enum):
    IN_NOTHING = 0
    IN_SINGLE_QUOTE = 1
    IN_DOUBLE_QUOTE = 2
    IN_TEXT = 3
    IN_NUMERIC = 4
    IN_SYMBOL = 5

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
        self.tk_type = Token.INPUT_END
        self.text = ''
        self._lno = 0
        self._col = 0
        self.tokens = [] # TokenItem[]
        self.state = ScanContext.IN_NOTHING
        self.info = {}
        self.valid_symbols = "!@#$%^&*-+=[]{};:|\\?><,./"
        self.single_quote = "'"
        self.double_quote = '"'
        self.digits = "0123456789"
        self.hexdigits = "AaBbCcDdEeFf"

    def reset(self):
        self.tk_type = Token.INPUT_END
        self.text = ''
        self._lno = 0
        self._col = 0
        self.state = ScanContext.IN_NOTHING
        self.info = {}
    
    def mark_end_of_input(self):
        self.add_token(Token.INPUT_END)

    def isalpha(self, char):
        return char.isalpha()

    def isnumeric(self, char):
        return self.digits.find(char) >= 0

    def ishexdigit(self, char):
        return self.hexdigits.find(char) >= 0

    def issymbol(self, char):
        return self.valid_symbols.find(char) >= 0

    def istoken(self):
        return self.tk_type != Token.INPUT_END

    def get_text(self):
        return self.text

    def get_tokens(self):
        return self.tokens

    def add_token(self, tk, s=''):
        new_tk = TokenItem(tk, s)
        if tk != Token.INPUT_END:
            new_tk.set_meta(self._lno, self._col)
        self.tokens.append(new_tk)
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
            self.state = ScanContext.IN_SYMBOL
            self.tk_type = Token.SYMBOL
            self.text = char
            # self.add_token(Token.SYMBOL, char)
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
        
    def did_handle_symbol(self, char):
        if self.issymbol(char):
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

    def set_meta(self, line, col):
        self._lno = line
        self._col = col

    def did_handle_char(self, char, lno, col):
        state = self.state
        if state == ScanContext.IN_NOTHING:
            self.set_meta(lno, col)
            return self.did_handle_undetermined(char)
        elif state == ScanContext.IN_DOUBLE_QUOTE:
            return self.did_handle_quoted(char, self.double_quote)
        elif state == ScanContext.IN_SINGLE_QUOTE:
            return self.did_handle_quoted(char, self.single_quote)
        elif state == ScanContext.IN_SYMBOL:
            return self.did_handle_symbol(char)
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

# tk: Tokenizer
def tokenize_line(tk, lno, char_iter):    

    # tk.add_token(Token.LINE_BEGIN, str(lno))

    # Iterate over the characters
    col = 0
    for char in char_iter:
        col = col + 1
        handled = False
        while not handled:
            handled = tk.did_handle_char(char, lno, col)

    # Done with all chars being handled somehow
    # Drain the tokenizer
    if tk.istoken():
        tk.emit_token()

    tk.set_meta(lno, col + 1)
    tk.add_token(Token.LINE_END)
    #return tk.get_tokens()

def tokenize_program(file_path):
    should_join = False
    all_lines = lines_to_process(file_path, should_join)
    lno = 0
    tk = Tokenizer()
    for line in all_lines:
        lno = lno + 1
        print("[%4d] %s" % (lno, line))
        if not line.startswith("//") and len(line) > 0:
            char_iter = itertools.islice(line, 0, None)
            more_tokens = tokenize_line(tk, lno, char_iter)

    lx = len(all_lines)
    suffix = 's'
    if lx == 1:
        suffix = ''
    print('Processed %d line%s from "%s"' % (lx, suffix, file_path))
    print("")

    tk.mark_end_of_input()

    return (tk.get_tokens(), all_lines)
