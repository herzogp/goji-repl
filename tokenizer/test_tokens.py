import itertools
import pytest

from tokenizer.tokens import (
    tokenize_program, 
    Token, 
    TokenItem,
)

from tokenizer.tools import (
    lines_to_process, 
    show_token_diff,
    # show_tokens,
)

@pytest.fixture
def basic_tokens():
    # (= x1(a b) (+ a b))
    expected_1 = [
        TokenItem(Token.LINE_BEGIN, '2'),
        TokenItem(Token.LIST_BEGIN),
        TokenItem(Token.SYMBOL, '='),
        TokenItem(Token.LIST_BEGIN),
        TokenItem(Token.TEXT, 'x1'),
        TokenItem(Token.TEXT, 'a'),
        TokenItem(Token.TEXT, 'b'),
        TokenItem(Token.LIST_END),
        TokenItem(Token.LIST_BEGIN),
        TokenItem(Token.SYMBOL, '+'),
        TokenItem(Token.TEXT, 'a'),
        TokenItem(Token.TEXT, 'b'),
        TokenItem(Token.LIST_END),
        TokenItem(Token.LIST_END),
        TokenItem(Token.LINE_END),
    ]
    
    # (= x2(b) (* b b))
    expected_2 = [
        TokenItem(Token.LINE_BEGIN, '3'),
        TokenItem(Token.LIST_BEGIN),
        TokenItem(Token.SYMBOL, '='),
        TokenItem(Token.LIST_BEGIN),
        TokenItem(Token.TEXT, 'x2'),
        TokenItem(Token.TEXT, 'b'),
        TokenItem(Token.LIST_END),
        TokenItem(Token.LIST_BEGIN),
        TokenItem(Token.SYMBOL, '*'),
        TokenItem(Token.TEXT, 'b'),
        TokenItem(Token.TEXT, 'b'),
        TokenItem(Token.LIST_END),
        TokenItem(Token.LIST_END),
        TokenItem(Token.LINE_END),
    ]
    
    # (  x1 "abc"  7   'xyz'   )
    expected_3 = [
        TokenItem(Token.LINE_BEGIN, '6'),
        TokenItem(Token.LIST_BEGIN),
        TokenItem(Token.TEXT, 'x1'),
        TokenItem(Token.QTEXT, 'abc'),
        TokenItem(Token.NUMERIC, '7'),
        TokenItem(Token.QTEXT, 'xyz'),
        TokenItem(Token.LIST_END),
        TokenItem(Token.LINE_END),
    ]
    
    # (x2 (x1 40.1 52))
    expected_4 = [
        TokenItem(Token.LINE_BEGIN, '7'),
        TokenItem(Token.LIST_BEGIN, ''),
        TokenItem(Token.TEXT, 'x2'),
        TokenItem(Token.LIST_BEGIN, ''),
        TokenItem(Token.TEXT, 'x1'),
        TokenItem(Token.NUMERIC, '40.1'),
        TokenItem(Token.NUMERIC, '52'),
        TokenItem(Token.LIST_END, ''),
        TokenItem(Token.LIST_END, ''),
        TokenItem(Token.LINE_END),
    ]

    return expected_1 + expected_2 + expected_3 + expected_4


#  Test the tokenizer
class TestTokenizer:
    def test_basic_tokenizer(self, basic_tokens):
        all_tokens = tokenize_program("testdata/prog.ph")
        # ----------------------------------------------------------------------
        # To always see stdout output invoke as `pytest -s`
        # Remember to import show_tokens at the top of this file
        # show_tokens('Want Basic Tokens', basic_tokens)
        # show_tokens('Got All Tokens', all_tokens)
        # ----------------------------------------------------------------------
    
        if all_tokens != basic_tokens:
            failed = show_token_diff(all_tokens, basic_tokens)
            print('%i failed comparison(s)' % failed)

        assert all_tokens == basic_tokens
