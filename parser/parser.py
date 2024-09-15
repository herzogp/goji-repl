from typing import Union

from options import GojiOptions

from parser.symbols import (
    SymbolType,
    SymToken,
    # symbolized,
)

class Parser:
    def __init__(self, symtokens: list[SymToken], all_lines: list[str], options: GojiOptions) -> None:
        if options.show_tokens:
            print("initializing parser with %d tokens" % len(symtokens))
        self._symtokens = symtokens
        self._pos = 0
        self._ntx = len(symtokens)
        self._options = options
        self._all_lines = all_lines

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
        return self.token_at_index(self._pos)

    def token_at_index(self, idx) -> Union[SymToken, None]:
        if not self.has_tokens():
            return None
        if (idx < 0):
            return None
        return self._symtokens[idx]

    def peek_prev_token(self) -> Union[SymToken, None]:
        return self.token_at_index(self._pos - 1)

    def peek_next_token(self) -> Union[SymToken, None]:
        return self.token_at_index(self._pos + 1)

    def skip_one(self, type_to_skip: SymbolType, err_msg='') -> None:
        if self.show_parsing:
            print("[S1] ENTER skip_one(%s) - curent_pos: %d" % (type_to_skip, self._pos))
        symtok = self.current_token()
        if symtok is None:
            if err_msg == '':
                err_msg = "[S1] End of Tokens - unable to skip_one()"
            raise Exception(err_msg)
        elif symtok.is_input_end():
            self.advance()
        elif symtok.symtype != type_to_skip:
            if err_msg == '':
                err_msg = "[S1] Expected %s - saw %s" % (type_to_skip.name, symtok)
            raise Exception(err_msg)
        if self.show_parsing:
            print("[S1] Did successfully skip %s" % type_to_skip)
        self.advance()
        if self.show_parsing:
            print("[S1] Now advanced to %s" % self.current_token())
            print("")
        return None

    def skip_many(self, type_to_skip: SymbolType) -> None:
        if self.show_parsing:
            print("[SM] ENTER skip_many(%s)" % type_to_skip)
        skipping = True
        while skipping:
            symtok = self.current_token()
            if self.show_parsing:
                print("[SM] considering %s" % symtok)
            if symtok is None:
                skipping = False
            elif symtok.is_input_end():
                self.advance()
                skipping = False
            elif symtok.symtype != type_to_skip:
                skipping = False
            else:
                if self.show_parsing:
                    print("[SM] skip_many is skipping: %s" % symtok)
                self.advance()
        if self.show_parsing:
            print("[SM] skip_many advanced to %s" % self.current_token())
        return

    def skip_over(self, type_to_skip: SymbolType, err_msg='') -> None:
        if self.show_parsing:
            print("[SV] ENTER skip_over(%s) - curent_pos: %d" % (type_to_skip, self._pos))
        skipping = True
        if type_to_skip == SymbolType.LINE_END:
            skipping = False

        if skipping:
            self.skip_many(SymbolType.LINE_END)
        if self.show_parsing:
            print("[SV] skip_over(%s) - after possible skipping, curent_pos: %d" % (type_to_skip, self._pos))
            print("[SV] skip_over asking [S1] skip_one() to match next: ", type_to_skip)
        self.skip_one(type_to_skip, err_msg)

    def backup(self) -> None:
        oldpos = self._pos
        idx = self._pos - 1
        if idx >= 0:
            self._pos = idx
        return

    def advance(self) -> None:
        oldpos = self._pos
        idx = self._pos + 1
        if idx <= self._ntx:
            self._pos = idx
        return

    def advance_to_sym(self, sym: SymbolType) -> None:
        symtok = self.current_token()
        if symtok is None:
            return
        the_type = symtok.symtype
        while the_type != sym:
            if the_type == SymbolType.INPUT_END:
                return
            self.advance()
            symtok = self.current_token()
            if symtok is None:
                return
            the_type = symtok.symtype

    # starts peeking just beyond the current_token() position
    def peek_many(self, type_to_skip: SymbolType) -> Union[SymToken, None]:
        if self.show_parsing:
            print("[P*] ENTER peek_many(%s)" % type_to_skip)
        skipping = True
        idx = self._pos + 1
        while skipping:
            symtok = self.token_at_index(idx)
            if self.show_parsing:
                print("[P*] considering %s" % symtok)
            if symtok is None:
                skipping = False
            elif symtok.is_input_end():
                skipping = False
            elif symtok.symtype != type_to_skip:
                skipping = False
            else:
                if self.show_parsing:
                    print("[P*] peek_many is skipping: %s" % symtok)
                idx = idx + 1
        symtok_found = self.token_at_index(idx)
        if self.show_parsing:
            print("[P*] peek_many advanced to %s" % symtok_found)
        return symtok_found
