from typing import Union

from parser.symbols import (
    # SymbolType,
    SymToken,
    # symbolized,
)

class Parser:
    #def __init__(self, symtokens: list[SymToken], rule_provider: RuleProvider) -> None:
    def __init__(self, symtokens: list[SymToken]) -> None:
        print("initializing parser with %d tokens" % len(symtokens))
        self._symtokens = symtokens
        self._pos = 0
        self._ntx = len(symtokens)
        # [PH] self._rule_provider = rule_provider

    # [PH] @property
    # [PH] def rule_provider(self) -> RuleProvider:
    # [PH]     return self._rule_provider

    def has_tokens(self) -> bool:
        return self._pos < self._ntx

    def current_token(self) -> Union[SymToken, None]:
        if not self.has_tokens():
            print("current_token() -> None")
            return None
        print("pos: %d current_token() -> %s" % (self._pos, self._symtokens[self._pos]))
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
        print("skip_one")
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
        print("advance: %d to %d" % (oldpos, self._pos))
        return
