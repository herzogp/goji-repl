from typing import Union

from options import GojiOptions

from parser.symbols import (
    # SymbolType,
    SymToken,
    # symbolized,
)

class Parser:
    def __init__(self, symtokens: list[SymToken], options: GojiOptions) -> None:
        if options.show_tokens:
            print("initializing parser with %d tokens" % len(symtokens))
        self._symtokens = symtokens
        self._pos = 0
        self._ntx = len(symtokens)
        self._options = options

    @property
    def show_tokens(self) -> bool:
        return self._options.show_tokens

    @property
    def show_rules(self) -> bool:
        return self._options.show_rules

    @property
    def show_parsing(self) -> bool:
        return self._options.show_parsing

    def has_tokens(self) -> bool:
        return self._pos < self._ntx

    def current_token(self) -> Union[SymToken, None]:
        if not self.has_tokens():
            if options.show_tokens:
                print("current_token() -> None")
            return None
        # if self.show_tokens:
        #     print("pos: %d current_token() -> %s" % (self._pos, self._symtokens[self._pos]))
        return self._symtokens[self._pos]

    def peek_prev_token(self) -> Union[SymToken, None]:
        idx = self._pos - 1
        if idx >= 0:
            symtok = self._symtokens[idx]
            return symtok
        return None

    def peek_next_token(self) -> Union[SymToken, None]:
        idx = self._pos + 1
        if idx < self._ntx:
            symtok = self._symtokens[idx]
            return symtok
        return None

    def skip_one(self, type_to_skip, err_msg='') -> None:
        symtok = self.current_token()
        if symtok is None:
            if err_msg == '':
                err_msg = "End of Tokens - unable to skip_one()"
            raise Exception(err_msg)
        if symtok.symtype != type_to_skip:
            if err_msg == '':
                err_msg = "Expected %s - saw %s" % (type_to_skip.name, symtok)
            raise Exception(err_msg)
        self.advance()

    def advance(self) -> None:
        oldpos = self._pos
        idx = self._pos + 1
        if idx <= self._ntx:
            self._pos = idx
        # if self.show_tokens:
        #     print("advance: %d to %d" % (oldpos, self._pos))
        return
