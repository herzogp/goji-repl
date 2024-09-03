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
        TokenItem(Token.LIST_BEGIN).set_meta(2,1),
        TokenItem(Token.SYMBOL, '=').set_meta(2,2),
        TokenItem(Token.LIST_BEGIN).set_meta(2,4),
        TokenItem(Token.TEXT, 'x1').set_meta(2,5),
        TokenItem(Token.TEXT, 'a').set_meta(2,8),
        TokenItem(Token.TEXT, 'b').set_meta(2,10),
        TokenItem(Token.LIST_END).set_meta(2,11),
        TokenItem(Token.LIST_BEGIN).set_meta(2,13),
        TokenItem(Token.SYMBOL, '+').set_meta(2,14),
        TokenItem(Token.TEXT, 'a').set_meta(2,16),
        TokenItem(Token.TEXT, 'b').set_meta(2,18),
        TokenItem(Token.LIST_END).set_meta(2,19),
        TokenItem(Token.LIST_END).set_meta(2,20),
        TokenItem(Token.LINE_END).set_meta(2,21),
    ]
    
    # (= x2(b) (* b b))
    expected_2 = [
        TokenItem(Token.LIST_BEGIN).set_meta(3,1),
        TokenItem(Token.SYMBOL, '=').set_meta(3,2),
        TokenItem(Token.LIST_BEGIN).set_meta(3,4),
        TokenItem(Token.TEXT, 'x2').set_meta(3,5),
        TokenItem(Token.TEXT, 'b').set_meta(3,8),
        TokenItem(Token.LIST_END).set_meta(3,9),
        TokenItem(Token.LIST_BEGIN).set_meta(3,11),
        TokenItem(Token.SYMBOL, '*').set_meta(3,12),
        TokenItem(Token.TEXT, 'b').set_meta(3,14),
        TokenItem(Token.TEXT, 'b').set_meta(3,16),
        TokenItem(Token.LIST_END).set_meta(3,17),
        TokenItem(Token.LIST_END).set_meta(3,18),
        TokenItem(Token.LINE_END).set_meta(3,19),
    ]
    
    # (  x1 "abc"  7   'xyz'   )
    expected_3 = [
        TokenItem(Token.LIST_BEGIN).set_meta(6,1),
        TokenItem(Token.TEXT, 'x1').set_meta(6,4),
        TokenItem(Token.QTEXT, 'abc').set_meta(6,7),
        TokenItem(Token.NUMERIC, '7').set_meta(6,14),
        TokenItem(Token.QTEXT, 'xyz').set_meta(6,18),
        TokenItem(Token.LIST_END).set_meta(6,26),
        TokenItem(Token.LINE_END).set_meta(6,27),
    ]
    
    # (x2 (x1 40.1 52))
    expected_4 = [
        TokenItem(Token.LIST_BEGIN, '').set_meta(7,1),
        TokenItem(Token.TEXT, 'x2').set_meta(7,2),
        TokenItem(Token.LIST_BEGIN, '').set_meta(7,5),
        TokenItem(Token.TEXT, 'x1').set_meta(7,6),
        TokenItem(Token.NUMERIC, '40.1').set_meta(7,9),
        TokenItem(Token.NUMERIC, '52').set_meta(7,14),
        TokenItem(Token.LIST_END, '').set_meta(7,16),
        TokenItem(Token.LIST_END, '').set_meta(7,17),
        TokenItem(Token.LINE_END).set_meta(7,18),
    ]

    expected_end = [
        TokenItem(Token.INPUT_END),
    ]

    return expected_1 + expected_2 + expected_3 + expected_4 + expected_end


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
