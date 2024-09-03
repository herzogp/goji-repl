import pytest

# from p1 import *
from env import (
    EnvItem,
    EnvTable,
    # ItemType,
    nil,
)

from tokenizer.tokens import (
    Token, 
)

from node import (
    make_atom_node,
)

#  Test the EnvItem support
class TestEnvItem:
    def test_env_number_item(self):
        num_item = EnvItem("v-number", make_atom_node(Token.NUMERIC, '30'))
        got = str(num_item)
        want = 'v-number: %i' % 30
        assert got == want

    def test_env_empty_number_item(self):
        num_item = EnvItem("v-number", make_atom_node(Token.NUMERIC, '0'))
        got = str(num_item)
        want = 'v-number: %i' % 0
        assert got == want

    def test_env_text_item(self):
        text_item = EnvItem("v-text", make_atom_node(Token.TEXT, "abc"))
        got = str(text_item)
        want = "v-text: %s" % 'abc'
        assert got == want

    def test_env_empty_text_item(self):
        text_item = EnvItem("v-text", make_atom_node(Token.TEXT, ""))
        got = str(text_item)
        want = "v-text: %s" % ''
        assert got == want

    def test_env_nil_item(self):
        nil_item = EnvItem('nil', make_atom_node(Token.INPUT_END))
        got = str(nil_item)
        want = 'nil'
        assert got == want

    def test_env_nil_class_item(self):
        got = str(nil)
        want = 'nil'
        assert got == want

    @pytest.mark.skip(reason="No list support yet")
    def test_env_list_item(self):
        list_item = EnvItem("v-list", ItemType.LIST, (10, 'a', 'b', 12.3,))
        got = str(list_item)
        want = "v-list: (10, 'a', 'b', 12.3)"
        assert got == want

    @pytest.mark.skip(reason="No list support yet")
    def test_env_empty_list_item(self):
        list_item = EnvItem("v-empty-list", ItemType.LIST)
        got = str(list_item)
        want = 'v-empty-list: ()'
        assert got == want

    @pytest.mark.skip(reason="No list support yet")
    def test_env_list_with_sublist(self):
        list_item = EnvItem("v-list", ItemType.LIST, (10, 'a', 'b', ('g', 41, ),))
        got = str(list_item)
        want = "v-list: (10, 'a', 'b', ('g', 41))"
        assert got == want

    @pytest.mark.skip(reason="No list support yet")
    def test_env_list_with_empty_sublist(self):
        list_item = EnvItem("v-list", ItemType.LIST, (10, 'a', 'b', tuple(),))
        got = str(list_item)
        want = "v-list: (10, 'a', 'b', ())"
        assert got == want


@pytest.fixture
def empty_env():
    return EnvTable()

@pytest.fixture
def root_env():
    e = EnvTable()
    num_item = EnvItem("a-number", make_atom_node(Token.NUMERIC, '30'))
    some_num_item = EnvItem("some-value", make_atom_node(Token.NUMERIC, '794'))
    text_item = EnvItem("a-text", make_atom_node(Token.TEXT, "abc"))
    e.set_item(num_item)
    e.set_item(some_num_item)
    e.set_item(text_item)
    return e

@pytest.fixture
def child_env(root_env):
    e = EnvTable(root_env)
    another_num_item = EnvItem("another-number", make_atom_node(Token.NUMERIC, '19'))
    another_text_item = EnvItem("another-text", make_atom_node(Token.TEXT, "xyz reading"))
    override_num_item = EnvItem("v-number", make_atom_node(Token.NUMERIC, '1014'))
    some_text_item = EnvItem("some-value", make_atom_node(Token.TEXT, 'textual now'))
    e.set_item(another_num_item)
    e.set_item(another_text_item)
    e.set_item(override_num_item)
    e.set_item(some_text_item)
    return e

#  Test the EnvTable support
class TestEnvTable:
    def test_empty_table_size(self, empty_env):
        root_count = empty_env.size
        assert root_count == 0

    def test_table_size(self, root_env):
        root_count = root_env.size
        assert root_count == 3

    def test_add_nil_item(self, root_env):
        old_count = root_env.size
        root_env.set_item(nil)
        root_env.set_item(EnvItem("nil", make_atom_node(Token.INPUT_END)))
        new_count = root_env.size
        assert old_count == new_count

    def test_item_found(self, root_env):
        found_item = root_env.get_item("a-number")
        assert found_item != None
        assert found_item.name == "a-number"

    def test_item_not_found_in_empty_env(self, empty_env):
        found_item = empty_env.get_item("a-number")
        assert found_item == None

    def test_unknown_item_not_found(self, root_env):
        found_item = root_env.get_item("x-number")
        assert found_item == None

