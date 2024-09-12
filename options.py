class GojiOptions:
    def __init__(self, args):
        self._show_parsing = args.show_parsing
        self._show_rules = args.show_rules
        self._show_tokens = args.show_tokens
        self._program_file = args.program_file

    @property
    def show_rules(self) -> bool:
        return self._show_rules

    @property
    def show_tokens(self) -> bool:
        return self._show_tokens

    @property
    def show_parsing(self) -> bool:
        return self._show_parsing

    @property
    def program_file(self) -> str:
        return self._program_file

